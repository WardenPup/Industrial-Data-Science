"""Post-review MSM, split-boundary and exported-result verification."""
import hashlib,json,os,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.tools/matplotlib'))
import numpy as np
import pandas as pd
from aeon.distances import msm_cost_matrix
from aeon.clustering import KASBA,TimeSeriesKMeans
from sklearn.metrics import adjusted_rand_score,normalized_mutual_info_score
from sessions.ch12 import clustering as study


def main():
    out=ROOT/'outputs/ch12/exercise_12_1'
    x=np.array([1.,1.,3.]);y=np.array([1.,3.])
    hand=np.array([[0.,3.],[1.,2.],[4.,1.]])
    np.testing.assert_array_equal(study.msm_matrix(x,y),hand)
    np.testing.assert_array_equal(msm_cost_matrix(x,y,c=1.),hand)
    np.testing.assert_array_equal(pd.read_csv(out/'msm_example.csv',index_col=0).to_numpy(),hand)
    rng=np.random.default_rng(73)
    for n,m,c in [(2,4,.5),(4,3,1.),(5,5,2.)]:
        a,b=rng.normal(size=n),rng.normal(size=m)
        np.testing.assert_allclose(study.msm_matrix(a,b,c),msm_cost_matrix(a,b,c=c),rtol=1e-13,atol=1e-12)
    raw_train,truth_train=study.load_gestures('TRAIN')
    raw_test,truth_test=study.load_gestures('TEST')
    expected_train=study.resample_normalize(raw_train)
    expected_test=study.resample_normalize(raw_test)
    calls=[]
    class Audited:
        def __init__(self,estimator):self.estimator=estimator
        def __getattr__(self,name):return getattr(self.estimator,name)
        def fit(self,*args,**kwargs):
            assert len(args)==1 and not kwargs
            np.testing.assert_array_equal(args[0],expected_train)
            calls.append({'method':type(self.estimator).__name__,'operation':'fit','shape':list(args[0].shape),'labels_supplied':False})
            self.estimator.fit(args[0]);return self
        def predict(self,*args,**kwargs):
            assert len(args)==1 and not kwargs
            np.testing.assert_array_equal(args[0],expected_test)
            calls.append({'method':type(self.estimator).__name__,'operation':'predict','shape':list(args[0].shape),'labels_supplied':False})
            return self.estimator.predict(args[0])
    with patch.object(study,'TimeSeriesKMeans',lambda **kw:Audited(TimeSeriesKMeans(**kw))),patch.object(study,'KASBA',lambda **kw:Audited(KASBA(**kw))):
        raw,prepared,models,metrics,assignments=study.run_experiment()
    assert len(calls)==4
    original=pd.read_csv(out/'assignments.csv',dtype={'class':str})
    pd.testing.assert_frame_equal(assignments,original)
    saved=pd.read_csv(out/'metrics.csv')
    np.testing.assert_allclose(metrics[['ARI','NMI']],saved[['ARI','NMI']],atol=1e-12)
    for _,row in metrics.iterrows():
        a=assignments[(assignments.method==row.method)&(assignments.split==row.split)]
        expected=truth_train if row.split=='TRAIN' else truth_test
        np.testing.assert_array_equal(a['class'],expected)
        np.testing.assert_allclose(row.ARI,adjusted_rand_score(expected,a.cluster),atol=1e-12)
        np.testing.assert_allclose(row.NMI,normalized_mutual_info_score(expected,a.cluster),atol=1e-12)
        # Both metrics ignore arbitrary cluster numbering.
        np.testing.assert_allclose(row.ARI,adjusted_rand_score(expected,5-a.cluster),atol=1e-12)
        np.testing.assert_allclose(row.NMI,normalized_mutual_info_score(expected,5-a.cluster),atol=1e-12)
    for i,name in enumerate(models):
        for split in ['TRAIN','TEST']:
            subset=original[(original.method==name)&(original.split==split)]
            counts=pd.crosstab(subset['class'],subset.cluster).reindex(columns=range(6),fill_value=0)
            saved_counts=pd.read_csv(out/f'counts_{i}_{split}.csv',index_col=0)
            np.testing.assert_array_equal(counts.to_numpy(),saved_counts.to_numpy())
    for split,expected in [(raw_train,(115,455)),(raw_test,(100,375))]:
        assert (min(v.shape[-1] for v in split),max(v.shape[-1] for v in split))==expected
    manifest=json.loads((out/'validation_manifest.json').read_text())
    for file,digest in manifest['files'].items():assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,file
    report={'ai_assistance':'Codex','human_independent_execution_claimed':False,'full_msm_example_matrix':hand.tolist(),
            'full_library_cost_matrices_checked':4,'runtime_fit_predict_calls':calls,
            'assignments_exactly_reproduced':True,'metrics_recalculated':metrics[['method','split','ARI','NMI']].to_dict(orient='records'),
            'cluster_id_permutation_invariance':True,'all_four_cross_tables_match':True,'manifest_hashes_checked':len(manifest['files']),
            'limitations':'One seed; no stability study or new-person generalization. Library reference is not an independent reimplementation of aeon.'}
    (out/'human_review_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: complete MSM example/random matrices, TRAIN-only label-free fits, TEST-only predictions, exact repeated assignments, ARI/NMI permutation invariance, cross tables and 16 hashes')

if __name__=='__main__':main()
