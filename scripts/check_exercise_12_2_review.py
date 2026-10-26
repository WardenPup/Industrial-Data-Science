"""Post-review full-data audit; no model or hyperparameter selection."""
from pathlib import Path
from unittest.mock import patch
import inspect,json,hashlib,os,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.tools/matplotlib'))
import numpy as np
import pandas as pd
import torch
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier
from sessions.ch12 import classification as study


def main():
    out=ROOT/'outputs/ch12/exercise_12_2'
    train,y_train=study.load_uwave('TRAIN');test,y_test=study.load_uwave('TEST')
    assert train.shape==(120,3,315) and test.shape==(320,3,315)
    mean=train.mean(axis=(0,2),keepdims=True);scale=train.std(axis=(0,2),ddof=0,keepdims=True)
    prepared_train=np.ascontiguousarray((train-mean)/scale,dtype=np.float32)
    prepared_test=np.ascontiguousarray((test-mean)/scale,dtype=np.float32)
    calls=[];actual_cnn={}
    class AuditedKNN:
        def __init__(self,**params):
            assert params=={'n_neighbors':3,'weights':'uniform','distance':'dtw','distance_params':{'window':.1},'n_jobs':1}
            self.model=KNeighborsTimeSeriesClassifier(**params)
        def fit(self,*args,**kwargs):
            assert len(args)==2 and not kwargs
            np.testing.assert_array_equal(args[0],prepared_train);np.testing.assert_array_equal(args[1],y_train)
            calls.append({'method':'DTW 3-NN','operation':'fit','shape':list(args[0].shape),'labels':'TRAIN only'})
            self.model.fit(*args);return self
        def predict(self,x):
            np.testing.assert_array_equal(x,prepared_test)
            calls.append({'method':'DTW 3-NN','operation':'predict','shape':list(x.shape),'labels_supplied':False})
            return self.model.predict(x)
    real_cnn=study.fit_cnn
    def audited_cnn(*args,**kwargs):
        bound=inspect.signature(real_cnn).bind(*args,**kwargs);bound.apply_defaults()
        np.testing.assert_array_equal(bound.arguments['x_train'],prepared_train)
        np.testing.assert_array_equal(bound.arguments['y_encoded'],np.unique(y_train,return_inverse=True)[1])
        assert bound.arguments['epochs']==60 and bound.arguments['seed']==42 and bound.arguments['n_classes']==8
        actual_cnn.update(epochs=60,seed=42,n_classes=8)
        calls.append({'method':'CNN','operation':'fit','shape':list(prepared_train.shape),'labels':'TRAIN only'})
        return real_cnn(*args,**kwargs)
    with patch.object(study,'KNeighborsTimeSeriesClassifier',AuditedKNN),patch.object(study,'fit_cnn',audited_cnn),patch.object(study,'fit_scaler',wraps=study.fit_scaler) as scaling,patch.object(torch,'manual_seed',wraps=torch.manual_seed) as seed:
        fitted=study.fit_classifiers(train,y_train)
        def audit_forward(module,args):
            assert len(args)==1
            np.testing.assert_array_equal(args[0].detach().cpu().numpy(),prepared_test)
            calls.append({'method':'CNN','operation':'forward in predict_classifiers','shape':list(prepared_test.shape),'labels_supplied':False})
        hook=fitted['cnn'].register_forward_pre_hook(audit_forward)
        try:
            predictions,predict_seconds,logits=study.predict_classifiers(fitted,test)
        finally:
            hook.remove()
        assert scaling.call_count==1;np.testing.assert_array_equal(scaling.call_args.args[0],train)
        seed.assert_called_once_with(42)
    np.testing.assert_array_equal(fitted['scaler'][0],mean);np.testing.assert_array_equal(fitted['scaler'][1],scale)
    assert sum(call['method']=='CNN' and call['operation']=='forward in predict_classifiers' for call in calls)==1
    saved=pd.read_csv(out/'predictions.csv',dtype={'true':str,'knn':str,'cnn':str})
    np.testing.assert_array_equal(saved.true,y_test)
    np.testing.assert_array_equal(saved.knn,predictions['DTW 3-NN']);np.testing.assert_array_equal(saved.cnn,predictions['CNN'])
    metrics,matrices,reports=study.evaluate(y_test,predictions,fitted['classes'])
    previous=pd.read_csv(out/'metrics.csv')
    np.testing.assert_allclose(metrics[['accuracy','balanced_accuracy','macro_f1']],previous[['accuracy','balanced_accuracy','macro_f1']],atol=1e-12)
    csv_report=pd.read_csv(out/'classification_report.csv',dtype={'class':str})
    pd.testing.assert_frame_equal(reports,csv_report,check_exact=False,atol=1e-12,rtol=1e-12)
    for name,column,correct,f1 in [('DTW 3-NN','knn',291,.908593),('CNN','cnn',271,.846505)]:
        matrix=matrices[name]
        np.testing.assert_array_equal(matrix,pd.read_csv(out/f'confusion_{column}.csv',index_col=0).to_numpy())
        assert int(np.trace(matrix))==correct and int(matrix[3,4])==11
        assert matrix[3,3]==(28 if name=='DTW 3-NN' else 25)
        score=metrics.set_index('method').loc[name]
        np.testing.assert_allclose(score.accuracy,correct/320,atol=1e-12)
        assert abs(score.macro_f1-f1)<.0000005
    assert all(matrices['DTW 3-NN'][i,i]==40 for i in [1,6,7])
    assert all(matrices['CNN'][i,i]==36 for i in [6,7])
    parameters=sum(p.numel() for p in fitted['cnn'].parameters() if p.requires_grad);assert parameters==5000
    history=pd.read_csv(out/'cnn_training.csv')
    np.testing.assert_allclose(history.train_cross_entropy,fitted['history'].train_cross_entropy,atol=1e-10,rtol=1e-10)
    assert history.epoch.tolist()==list(range(1,61))
    assert np.isfinite(history.train_cross_entropy).all()
    with np.load(out/'cnn_weights.npz',allow_pickle=False) as weights:
        for key,value in fitted['cnn'].state_dict().items():np.testing.assert_allclose(weights[key],value.numpy(),atol=1e-7,rtol=1e-6)
    manifest=json.loads((out/'validation_manifest.json').read_text())
    for file,digest in manifest['files'].items():assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,file
    report={'ai_assistance':'Codex','student_independent_execution_claimed':False,
            'train_shape':list(train.shape),'test_shape':list(test.shape),'actual_calls':calls,
            'actual_cnn_config':actual_cnn,'cnn_parameters':parameters,'all_640_predictions_reproduced':True,
            'all_reports_and_confusion_matrices_match':True,'metrics':metrics.to_dict(orient='records'),
            'training_curve':{'epochs':60,'first':float(history.train_cross_entropy.iloc[0]),'last':float(history.train_cross_entropy.iloc[-1]),'positive_increments':int((np.diff(history.train_cross_entropy)>0).sum()),'overfitting_proven':False},
            'runtime_comparison':{'previous':previous.to_dict(orient='records'),'repeat_fit_seconds':fitted['fit_seconds'],'repeat_predict_seconds':predict_seconds},
            'artifact_hashes_checked':len(manifest['files'])}
    (out/'human_review_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: actual TRAIN-only scaler and training calls, TEST-only predictions, 640 exact predictions, all reviewed counts/metrics/reports, 60-epoch curve, seed 42, 5000 parameters, weights and 12 artifact hashes')

if __name__=='__main__':main()
