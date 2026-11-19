"""Actual offline browser interactions, not programmatic replacement of user gestures."""
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"outputs/ch14/exercise_14_4"

def check():
    if (ROOT/".tools/playwright").exists():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH",str(ROOT/".tools/playwright"))
    results=[]
    expected={"Machine failure":339,"TWF":46,"HDF":115,"PWF":95,"OSF":98,"RNF":19}
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=["--enable-unsafe-swiftshader"])
        for width in [900,1400]:
            page=browser.new_page(viewport={"width":width,"height":1000},offline=True)
            errors,failures=[],[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.on("requestfailed",lambda r:failures.append(r.url))
            print(f"Starting offline browser {width}px", flush=True)
            page.goto((OUTPUT/"parallel_coordinates_notebook.html").as_uri())
            frame=page.frames[1]
            frame.wait_for_function("window.chartReady===true",timeout=60000)
            print("Chart initialized", flush=True)
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
            assert frame.evaluate("document.documentElement.scrollWidth<=innerWidth")
            def axis(label):
                return frame.locator(".axis-title").filter(has_text=label).last
            def brush(label,low=12,high=65):
                title=axis(label)
                title.scroll_into_view_if_needed()
                rect=title.locator("..").locator("..").locator(".axis-brush rect.background").bounding_box()
                page.mouse.move(rect["x"]+5,rect["y"]+low)
                page.mouse.down();page.mouse.move(rect["x"]+5,rect["y"]+high,steps=3);page.mouse.up()
            # Actual native dropdown selection and pointer brushing for all flags.
            for target,n in expected.items():
                print(f"Checking {width}px {target}", flush=True)
                frame.locator("#target").select_option(target)
                frame.wait_for_function("window.selectionReport.rows===10000")
                brush(target)
                frame.wait_for_function("window.selectionReport.rows==="+str(n),timeout=20000)
                result=frame.evaluate("window.selectionReport")
                assert result["positive"]==n
                results.append({"width":width,"action":"dropdown and pointer brush","target":target,**result})
                frame.locator("#reset").click()
                frame.wait_for_function("window.selectionReport.rows===10000")
            # Move HDF next to temperature difference by dragging its actual heading.
            frame.locator("#target").select_option("HDF")
            frame.locator("#scroll").evaluate("e=>e.scrollLeft=e.scrollWidth")
            a=axis("HDF").bounding_box();z=axis("ΔT [K]").bounding_box()
            page.mouse.move(a["x"]+a["width"]/2,a["y"]+a["height"]/2);page.mouse.down()
            page.mouse.move(z["x"]+z["width"]/2+65,a["y"]+a["height"]/2,steps=8);page.mouse.up()
            frame.wait_for_function("chart.data[0].dimensions[6].name==='failure'")
            brush("HDF")
            frame.wait_for_function("window.selectionReport.rows===115")
            results.append({"width":width,"action":"pointer reorder HDF after temp_diff and brush","order":frame.evaluate("chart.data[0].dimensions.map(d=>d.name)"),**frame.evaluate("window.selectionReport")})
            page.screenshot(path=str(ROOT/f".tools/14_4_html_{width}.png"),full_page=True)
            assert not errors and not failures,(errors,failures)
            page.close()
            print(f"PASS offline {width}px: six dropdown/brush/reset actions, pointer axis reorder, correct counts, no network/page errors or page overflow")
        # Standalone artifact also works without notebook or Python server.
        page=browser.new_page(viewport={"width":1500,"height":900},offline=True)
        page.goto((OUTPUT/"parallel_coordinates.html").as_uri())
        page.wait_for_function("window.chartReady===true",timeout=60000)
        for target,filename in [("HDF","01_hdf_brushed.png"),("PWF","02_pwf_brushed.png")]:
            page.locator("#target").select_option(target)
            page.wait_for_function("window.selectionReport.rows===10000")
            if target == "HDF":
                a=page.locator(".axis-title").filter(has_text="Drehzahl [rpm]").last.bounding_box()
                z=page.locator(".axis-title").filter(has_text="ΔT [K]").last.bounding_box()
                page.mouse.move(a["x"]+a["width"]/2,a["y"]+a["height"]/2);page.mouse.down()
                page.mouse.move(z["x"]+z["width"]/2-65,a["y"]+a["height"]/2,steps=8);page.mouse.up()
                page.wait_for_function("chart.data[0].dimensions[4].name==='Rotational speed [rpm]'")
            label=page.locator(".axis-title").filter(has_text=target).last
            rect=label.locator("..").locator("..").locator(".axis-brush rect.background").bounding_box()
            page.mouse.move(rect["x"]+5,rect["y"]+12);page.mouse.down();page.mouse.move(rect["x"]+5,rect["y"]+65,steps=3);page.mouse.up()
            page.wait_for_function("window.selectionReport.rows==="+str(expected[target]))
            results.append({"width":1500,"action":"standalone brush with reordered axes","target":target,"order":page.evaluate("chart.data[0].dimensions.map(d=>d.name)"),**page.evaluate("window.selectionReport")})
            page.screenshot(path=str(OUTPUT/filename),full_page=True)
        page.close();browser.close()
    (OUTPUT/"interaction_checks.json").write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    check()
