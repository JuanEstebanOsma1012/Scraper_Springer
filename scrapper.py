from playwright.sync_api import sync_playwright
import os

LINK="https://link.springer.com/search?new-search=true&query=%28HTCondor+OR+Condor%29+AND+%28HTC+OR+%28High+Throughput+Computing%29%29+AND+%28Universe+OR+%28Runtime+Environment%29%29+AND+%28Research+OR+Teaching+OR+Industry%29&content-type=research&date=custom&dateFrom=2005&dateTo=2024&sortBy=relevance"
DOWNLOAD_PATH="/home/juan/Documents/Trabajo de grado/SMS/referencias/"

def download_files():
    pagina = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(LINK)
        
        page.wait_for_timeout(5000)  # Esperar a que la página cargue

        while True:
            try:
                page.wait_for_selector("ol.u-list-reset", timeout=60000)
            except:
                print("Error: No se encontró la lista de resultados.")
                break

            for contador in range(1, 21):
                print(f"Procesando el artículo {pagina * 20 + contador}...")

                link = page.query_selector(f"a[data-track-context='{contador}']")
                if not link:
                    print(f"Advertencia: No se encontró el enlace para el contador {contador}")
                    continue

                link.click()
                page.wait_for_selector("div.c-bibliographic-information__column p.c-bibliographic-information__download-citation", timeout=60000)
                
                download_button = page.query_selector("div.c-bibliographic-information__column p.c-bibliographic-information__download-citation a")
                if not download_button:
                    print("Advertencia: No se encontró el botón de descarga.")
                    page.go_back()
                    page.wait_for_load_state('load')
                    continue

                with page.expect_download() as download_info:
                    download_button.click()
                    download = download_info.value
                    filename = os.path.join(DOWNLOAD_PATH, download.suggested_filename)
                    download.save_as(filename)
                
                page.go_back()
                page.wait_for_load_state('load')

            pagina += 1

            next_page = page.query_selector("a.eds-c-pagination__link[rel='next']")
            if not next_page:
                print("No hay más páginas disponibles.")
                break

            page.wait_for_timeout(2000)  # Pequeña pausa antes de hacer click
            next_page.click()
            page.wait_for_load_state('load')

        browser.close()

# Ejecutar el scrapper
download_files()