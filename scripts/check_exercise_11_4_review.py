"""Recheck reviewed values, actual STL arguments, candidate export and plot offsets."""
import os
from pathlib import Path
import sys,json,hashlib,math
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.tools/matplotlib'))
import numpy as np
import pandas as pd
import nbformat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from statsmodels.tsa.seasonal import STL
from sessions.ch11.production import load_production,DATA,SHA256
from sessions.ch11 import outliers


def main():
    source=load_production().pieces.copy()
    original=source.copy(deep=True)
    config={'period':52,'seasonal':13,'trend':101,'low_pass':53,'robust':True}
    with patch.object(outliers,'STL',wraps=STL) as spy:
        table,lower,upper=outliers.detect_outliers(source)
    assert spy.call_args.kwargs==config
    pd.testing.assert_series_equal(source,original)
    np.testing.assert_array_equal(table.pieces,source)
    reference=STL(source,**config).fit(inner_iter=2,outer_iter=15)
    np.testing.assert_allclose(table.residual,reference.resid,rtol=1e-13,atol=1e-12)
    residual=table.residual.to_numpy()
    mean=math.fsum(residual)/len(residual)
    std=math.sqrt(math.fsum((float(r)-mean)**2 for r in residual)/(len(residual)-1))
    mask=(residual<mean-3*std)|(residual>mean+3*std)
    np.testing.assert_array_equal(table.outlier_candidate,mask)
    candidates=table.loc[mask]
    output=ROOT/'outputs/ch11/exercise_11_4'
    exported=pd.read_csv(output/'outlier_candidates.csv',index_col='Date',parse_dates=True)
    assert exported.index.equals(candidates.index)
    np.testing.assert_allclose(exported.select_dtypes('number'),candidates.select_dtypes('number'),atol=1e-12)
    full=pd.read_csv(output/'components.csv',index_col='Date',parse_dates=True)
    assert full.index.equals(table.index)
    np.testing.assert_allclose(full.select_dtypes('number'),table.select_dtypes('number'),atol=1e-12)
    np.testing.assert_array_equal(full.outlier_candidate,mask)
    summary=json.loads((output/'summary.json').read_text())
    values={'observations':len(source),'missing':int(source.isna().sum()),'outlier_candidates':int(mask.sum()),
            'fraction_percent':100*mask.sum()/len(source),'negative_candidates':int((residual<lower).sum()),
            'positive_candidates':int((residual>upper).sum()),'residual_mean':mean,'residual_std_ddof1':std,
            'lower':mean-3*std,'upper':mean+3*std,
            'reconstruction_max_abs':float(np.max(np.abs(source-table.trend-table.seasonal-table.residual)))}
    for key,value in values.items(): np.testing.assert_allclose(summary[key],value,rtol=1e-12,atol=1e-12)
    for key,value in {'observations':1044,'missing':0,'outlier_candidates':26,'negative_candidates':26,'positive_candidates':0}.items(): assert values[key]==value
    for key,value in {'fraction_percent':2.4904,'residual_mean':-4.541,'residual_std_ddof1':26.820,'lower':-85.002,'upper':75.920}.items(): assert abs(values[key]-value)<.0005
    # Floating-point operation order can differ across platforms.
    reconstruction_tolerance=16*np.finfo(float).eps*max(1.,float(np.abs(source).max()))
    assert values['reconstruction_max_abs'] <= reconstruction_tolerance
    notebook=nbformat.read(ROOT/'sessions/ch11/production_outliers.ipynb',4)
    environment=dict(table=table,candidates=candidates,lower=lower,upper=upper,sns=sns,plt=plt,OUT=output,display=lambda *args:None)
    for cell,y in [(notebook.cells[2],'pieces'),(notebook.cells[3],'residual')]:
        with patch.object(plt,'show'),patch.object(matplotlib.figure.Figure,'savefig'):
            exec(cell.source,environment)
        ax=environment['ax']
        markers=[c for c in ax.collections if c.get_label().startswith("Ausreißerkandidaten")]
        assert len(markers)==1
        offsets=np.asarray(markers[0].get_offsets())
        assert len(offsets)==26
        np.testing.assert_allclose(offsets[:,0],mdates.date2num(candidates.index.to_pydatetime()))
        np.testing.assert_allclose(offsets[:,1],candidates[y])
        assert 'Stück/Woche' in ax.get_ylabel() and ax.get_xlabel()=='Jahr'
        plt.close(environment['fig'])
    manifest=json.loads((output/'validation_manifest.json').read_text())
    for file,digest in manifest['files'].items(): assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,file
    assert hashlib.sha256(DATA.read_bytes()).hexdigest()==SHA256
    report={'ai_assistance':'Codex','human_tests_claimed':False,'values':values,'actual_stl_config':config,
            'candidate_csv_and_both_plot_offsets_match':True,'manifest_files_checked':len(manifest['files']),
            'reference_note':'Direct STL reference uses same library; threshold arithmetic independently recomputed with math.fsum.'}
    (output/'human_review_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: actual STL arguments, unchanged raw observations, all reviewed numbers, both CSVs, 26 offsets in each plot and seven manifest hashes')

if __name__=='__main__': main()
