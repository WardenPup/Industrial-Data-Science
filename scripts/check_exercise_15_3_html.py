"""Actual offline dropdown, brushing, categorical filters and axis dragging."""
import os,json
from pathlib import Path
import pandas as pd
import numpy as np
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"outputs/ch15/exercise_15_3"
EXPECTED={"BEF":215,"CCF":344,"FWF":278,"WDF":300}

def check():
    if (ROOT/".tools/playwright").exists():os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH",str(ROOT/".tools/playwright"))
    records=[];bounds=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=["--enable-unsafe-swiftshader"])
        for width in [900,1400]:
            page=browser.new_page(viewport={"width":width,"height":1000},offline=True)
            errors=[];failed=[]
            page.on("pageerror",lambda e:errors.append(str(e)));page.on("requestfailed",lambda r:failed.append(r.url))
            print(f"Starting offline {width}px",flush=True)
            page.goto((OUTPUT/"parallel_coordinates_notebook.html").as_uri())
            frame=page.frames[1];frame.wait_for_function("window.chartReady===true",timeout=60000)
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
            assert frame.evaluate("document.documentElement.scrollWidth<=innerWidth")
            def axis(label):return frame.locator(".axis-title").filter(has_text=label).last
            def brush(label,low=12,high=65):
                title=axis(label);title.scroll_into_view_if_needed()
                r=title.locator("..").locator("..").locator(".axis-brush rect.background").bounding_box()
                page.mouse.move(r["x"]+5,r["y"]+low);page.mouse.down();page.mouse.move(r["x"]+5,r["y"]+high,steps=3);page.mouse.up()
            for target,n in EXPECTED.items():
                print(f"Checking {width}px {target}",flush=True)
                frame.locator("#target").select_option(target);frame.wait_for_function("window.selectionReport.rows===20000")
                brush(target);frame.wait_for_function("window.selectionReport.rows==="+str(n),timeout=20000)
                report=frame.evaluate("window.selectionReport");assert report["positive"]==n
                records.append({"width":width,"action":"dropdown and pointer brush","target":target,**report})
                if width==900:
                    for feature,span in report["bounds"].items():bounds.append({"Fehlertyp":target,"Merkmal":feature,"n":n,"Minimum":span[0],"Maximum":span[1]})
                frame.locator("#reset").click();frame.wait_for_function("window.selectionReport.rows===20000")
            frame.locator("#target").select_option("BEF")
            frame.locator("#scroll").evaluate("e=>e.scrollLeft=e.scrollWidth")
            a=axis("BEF").bounding_box();z=axis("Kühlung [%]").bounding_box()
            page.mouse.move(a["x"]+a["width"]/2,a["y"]+a["height"]/2);page.mouse.down()
            page.mouse.move(z["x"]+z["width"]/2+65,a["y"]+a["height"]/2,steps=8);page.mouse.up()
            frame.wait_for_function("chart.data[0].dimensions[6].name==='failure'")
            brush("BEF");frame.wait_for_function("window.selectionReport.rows===215")
            records.append({"width":width,"action":"pointer reorder after Cooling and brush","target":"BEF","order":frame.evaluate("chart.data[0].dimensions.map(d=>d.name)"),**frame.evaluate("window.selectionReport")})
            frame.locator("#target").select_option("FWF");frame.wait_for_function("window.selectionReport.rows===20000")
            brush("FWF");frame.wait_for_function("window.selectionReport.rows===278")
            brush("Material");frame.wait_for_function("window.selectionReport.rows===270")
            records.append({"width":width,"action":"FWF and Material N pointer brushes",**frame.evaluate("window.selectionReport")})
            brush("Bohrertyp",200,470);frame.wait_for_function("window.selectionReport.rows===9")
            report=frame.evaluate("window.selectionReport");assert report["failures"]["WDF"]==9
            records.append({"width":width,"action":"FWF Material N and drill N/H pointer brushes",**report})
            page.screenshot(path=str(ROOT/f".tools/15_3_html_{width}.png"),full_page=True)
            assert not errors and not failed,(errors,failed)
            page.close();print(f"PASS offline {width}px: four dropdown/brush/reset cases, pointer reorder and combined category brushes; correct counts/no network or page errors",flush=True)
        page=browser.new_page(viewport={"width":1500,"height":950},offline=True)
        page.goto((OUTPUT/"parallel_coordinates.html").as_uri());page.wait_for_function("window.chartReady===true",timeout=60000)
        for target,filename in [("BEF","01_bef_brushed.png"),("FWF","02_fwf_brushed.png")]:
            page.locator("#target").select_option(target);page.wait_for_function("window.selectionReport.rows===20000")
            title=page.locator(".axis-title").filter(has_text=target).last
            r=title.locator("..").locator("..").locator(".axis-brush rect.background").bounding_box()
            page.mouse.move(r["x"]+5,r["y"]+12);page.mouse.down();page.mouse.move(r["x"]+5,r["y"]+65,steps=3);page.mouse.up()
            page.wait_for_function("window.selectionReport.rows==="+str(EXPECTED[target]))
            records.append({"width":1500,"action":"standalone pointer brush","target":target,**page.evaluate("window.selectionReport")})
            page.wait_for_timeout(2000);page.screenshot(path=str(OUTPUT/filename),full_page=True)
        page.close();browser.close()
    raw=pd.read_csv(ROOT/"data/raw/XAI_Drilling_Dataset.csv")
    for row in bounds:
        v=raw.loc[raw[row["Fehlertyp"]].eq(1),row["Merkmal"]]
        assert len(v)==row["n"] and np.isclose(v.min(),row["Minimum"]) and np.isclose(v.max(),row["Maximum"])
    pd.DataFrame(bounds).to_csv(OUTPUT/"brushed_bounds.csv",index=False)
    (OUTPUT/"interaction_checks.json").write_text(json.dumps(records,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":check()
