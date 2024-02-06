import xlsxwriter as xw
import pandas as pd
from DBProcessor import DebugLogger as l
log=l.CreateLog()
def ExcelMarkup(output,Maand_Jaar,writer,SheetName):
    if output.empty:
        process = 0
        log.debug('|------->   Geen rijen voor: '+Maand_Jaar)
    else:
        log.debug('|------->   We verwerken nu data voor: '+Maand_Jaar)
        output.to_excel(writer,'%s' % SheetName)
        process = 1
        if process == 1:
            ######################################
            # get sheets to add the tables
            workbook  = writer.book
            worksheet_table_header = writer.sheets[SheetName]

            ######################################
            # the range in which the table is
            end_row = len(output.index)
            end_column = len(output.columns)
            cell_range = xw.utility.xl_range(0, 0, end_row, end_column)

            ######################################
            # This is optional when using a solid fill.
            Green_Format = workbook.add_format({'bg_color': 'green'})
            Green_Format = Green_Format.set_pattern(1)
                
            ######################################
            # The hack
            # Using the index in the Table
            output.reset_index(inplace=True)
            header = [{'header': di} for di in output.columns.tolist()]
            worksheet_table_header.add_table(cell_range,                                             {'header_row': True,                                              'first_column': True,                                              'autofilter': False,                                              'columns':header,                                              'style': 'Table Style Medium 9'})
                
            ######################################
            # This is optional when using a solid fill.
                
            White_Format = workbook.add_format({'color': '#FFFFFF'})
            White_Format.set_bold(True)
            White_Format.set_pattern(1)
            Green_Format = workbook.add_format({'bg_color': 'green'})
            LGreen_Format = workbook.add_format({'bg_color': '#FF99BB'})
            worksheet_table_header.set_column(0, 1, 0)
            worksheet_table_header.set_column(2, 2, 6)
            worksheet_table_header.set_column(3,3,17.4)
            worksheet_table_header.set_column(4, 5, 11)
            worksheet_table_header.set_column(6, 6, 8.2)
            worksheet_table_header.set_column(7, 7, 9.8)
            worksheet_table_header.set_column(8, 8, 4.4)
            worksheet_table_header.set_column(9, end_column-6, 2.5)
            worksheet_table_header.set_column(end_column-5,end_column-5,18)
            worksheet_table_header.set_column(end_column-4,end_column-4,22)
            worksheet_table_header.set_column(end_column-3,end_column-3,13)
            worksheet_table_header.set_column(end_column-2,end_column-2,18)
            worksheet_table_header.set_column(end_column-1,end_column,11)
            #worksheet_table_header.set_column(1, 1, None, Hidden_format)
            #worksheet_table_header.set_default_row(hide_unused_rows=True)
            worksheet_table_header.conditional_format('J2:AN800', {'type':'cell','criteria': '>=','value':1,'format': Green_Format})
            worksheet_table_header.conditional_format('J2:AN800', {'type':'cell','criteria': '>=','value':2,'format': White_Format})
            worksheet_table_header.conditional_format('C2:C800', {'type':'cell','criteria': '==','value':'"OK"','format': LGreen_Format})

            ######################################
            # The Outline Levels per type.
            #LogiStiek_Format = worksheet_table_header.set_row(None, None, None, {'level': 1})