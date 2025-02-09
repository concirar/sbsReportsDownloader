import flet as ft
from flet import Icons, Row, Text, ElevatedButton, FilePicker, FilePickerResultEvent, Page, Tabs, Tab, ProgressBar
import pandas as pd
import numpy as np
import sbsUtils as sbs
import os

def main(page: ft.Page):
    page.title = 'Download SBS Reports using flet. Developed by Arnold S. Condor - 2025'
    page.window.width = 600
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.DARK

    # Dropdowns for selection
    dfCalendarYears = pd.DataFrame({
        'Year': ['2021', '2022', '2023', '2024', '2025']
    })

    dfCalendarMonths = pd.DataFrame({
        'Month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    })

    dfReportsByTypeEnts = sbs.dfReportsByTypeEnts
    dictTypeEnts = dict(zip(dfReportsByTypeEnts['typeEntCode'], dfReportsByTypeEnts['typeEnt']))
    dictReports = dict(zip(dfReportsByTypeEnts['reportCode'], dfReportsByTypeEnts['reportName']))

    year_dropdown = ft.Dropdown(
        label="Select Year",
        options=[ft.dropdown.Option(year) for year in dfCalendarYears['Year']],
        value=dfCalendarYears['Year'][0]
    )

    month_dropdown = ft.Dropdown(
        label="Select Month",
        options=[ft.dropdown.Option(month) for month in dfCalendarMonths['Month']],
        value=dfCalendarMonths['Month'][0]
    )

    type_ent_dropdown = ft.Dropdown(
        label="Select Type Entity",
        options=[ft.dropdown.Option(key, value) for key, value in dictTypeEnts.items()],
        value=list(dictTypeEnts.keys())[0]
    )

    report_dropdown = ft.Dropdown(
        label="Select Report",
        options=[ft.dropdown.Option(key, value) for key, value in dictReports.items()],
        value=list(dictReports.keys())[0]
    )

    progress_bar = ProgressBar(width=400, height=20, value=0)
    progress_text = Text("")

    def download_report(e):
        import urllib.request
        pMonth = month_dropdown.value
        pAnio = year_dropdown.value
        pTypeEntCode = type_ent_dropdown.value
        pReportCode = report_dropdown.value
        pUrlSbsStats = sbs.pUrlSbsStats
        keyCalendarSbs = sbs.dfCalendar
        vNumMonth = keyCalendarSbs[keyCalendarSbs['numMonth'] == pMonth]['numMonth'].astype(str).values[0]
        vNameMonth = keyCalendarSbs[keyCalendarSbs['numMonth'] == pMonth]['nameMonth'].astype(str).values[0]
        vNameMonthShort = keyCalendarSbs[keyCalendarSbs['numMonth'] == pMonth]['nameMonthShort'].astype(str).values[0]
        vReportsByTypeEntCode = dfReportsByTypeEnts[
            (dfReportsByTypeEnts['typeEntCode'] == pTypeEntCode) & (dfReportsByTypeEnts['reportCode'] == pReportCode)
        ]['reportsByTypeEntCode'].astype(str).values[0]
        vFecRep = vNameMonthShort + pAnio
        urlSbsReport = pUrlSbsStats + pAnio + '/' + vNameMonth + '/' + vReportsByTypeEntCode + '-' + vFecRep + '.xls'
        
        file_path = f"{pTypeEntCode}_{pReportCode}_{pAnio}_{pMonth}_{vReportsByTypeEntCode}.xls"
        urllib.request.urlretrieve(urlSbsReport, file_path)
        progress_text.value = f"Report downloaded to {file_path}"
        page.update()

    download_button = ft.ElevatedButton(text="Download Report", on_click=download_report,bgcolor="#444444",color="#ffcc00")

    # Mass download section
    start_year_dropdown = ft.Dropdown(
        label="Start Year",
        options=[ft.dropdown.Option(year) for year in dfCalendarYears['Year']],
        value=dfCalendarYears['Year'][0]
    )

    start_month_dropdown = ft.Dropdown(
        label="Start Month",
        options=[ft.dropdown.Option(month) for month in dfCalendarMonths['Month']],
        value=dfCalendarMonths['Month'][0]
    )

    end_year_dropdown = ft.Dropdown(
        label="End Year",
        options=[ft.dropdown.Option(year) for year in dfCalendarYears['Year']],
        value=dfCalendarYears['Year'][0]
    )

    end_month_dropdown = ft.Dropdown(
        label="End Month",
        options=[ft.dropdown.Option(month) for month in dfCalendarMonths['Month']],
        value=dfCalendarMonths['Month'][0]
    )

    def download_mass_reports(e):
        import urllib.request
        pStartMonth = start_month_dropdown.value
        pStartAnio = start_year_dropdown.value
        pEndMonth = end_month_dropdown.value
        pEndAnio = end_year_dropdown.value
        pTypeEntCode = type_ent_dropdown.value
        pReportCode = report_dropdown.value
        pUrlSbsStats = sbs.pUrlSbsStats
        keyCalendarSbs = sbs.dfCalendar

        total_reports = (int(pEndAnio) - int(pStartAnio)) * 12 + (int(pEndMonth) - int(pStartMonth)) + 1
        progress_bar.value = 0
        page.update()

        # Logic to iterate over the date range and download reports
        report_count = 0
        for year in range(int(pStartAnio), int(pEndAnio) + 1):
            for month in range(1, 13):
                if year == int(pStartAnio) and month < int(pStartMonth):
                    continue
                if year == int(pEndAnio) and month > int(pEndMonth):
                    break
                pMonth = f"{month:02d}"
                vNumMonth = keyCalendarSbs[keyCalendarSbs['numMonth'] == pMonth]['numMonth'].astype(str).values[0]
                vNameMonth = keyCalendarSbs[keyCalendarSbs['numMonth'] == pMonth]['nameMonth'].astype(str).values[0]
                vNameMonthShort = keyCalendarSbs[keyCalendarSbs['numMonth'] == pMonth]['nameMonthShort'].astype(str).values[0]
                vReportsByTypeEntCode = dfReportsByTypeEnts[
                    (dfReportsByTypeEnts['typeEntCode'] == pTypeEntCode) & (dfReportsByTypeEnts['reportCode'] == pReportCode)
                ]['reportsByTypeEntCode'].astype(str).values[0]
                vFecRep = vNameMonthShort + str(year)
                urlSbsReport = pUrlSbsStats + str(year) + '/' + vNameMonth + '/' + vReportsByTypeEntCode + '-' + vFecRep + '.xls'
                
                file_path = f"{pTypeEntCode}_{pReportCode}_{year}_{pMonth}_{vReportsByTypeEntCode}.xls"
                urllib.request.urlretrieve(urlSbsReport, file_path)
                report_count += 1
                progress_bar.value = report_count / total_reports
                page.update()
                print(f"Report downloaded to {file_path}")

        progress_text.value = "Massive download completed."
        # Path where the file is downloaded using os.getcwd()
        progress_text.value = f"Reports downloaded to {os.getcwd()}"
        page.update()

    mass_download_button = ft.ElevatedButton(text="Download Massive Reports", on_click=download_mass_reports,bgcolor="#444444",color="#ffcc00")

    # Tabs for individual and massive reports
    tabs = Tabs(
        tabs=[
            Tab(
                text="Individual Report",
                content=ft.Column([
                    year_dropdown,
                    month_dropdown,
                    type_ent_dropdown,
                    report_dropdown,
                    download_button,
                    progress_text
                ])
            ),
            Tab(
                text="Massive Reports",
                content=ft.Column([
                    start_year_dropdown,
                    start_month_dropdown,
                    end_year_dropdown,
                    end_month_dropdown,
                    type_ent_dropdown,
                    report_dropdown,
                    mass_download_button,
                    progress_bar,
                    progress_text
                ])
            )
        ]
    )

    page.add(tabs)

if __name__ == '__main__':
    ft.app(target=main)