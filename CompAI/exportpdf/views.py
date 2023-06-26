from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import yaml

from sds.models import SDS
from esb.models import ESC

from django.http import HttpResponse
from reportlab.pdfgen import canvas


from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color
from reportlab.lib import colors
    
from datetime import date

class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width, self.height = LETTER

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if (self._pageNumber > 1):
                self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.drawImage("static/lr.png", self.width-inch*8-5, self.height-50, width=150, height=40, preserveAspectRatio=True)
        self.drawImage("static/ohka.png", self.width - inch * 2, self.height-50, width=100, height=45, preserveAspectRatio=True, mask='auto')
        self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Times-Roman', 10)
        self.drawString(LETTER[0]-x, 65, page)
        self.restoreState()

class PDFPSReporte:

    def __init__(self, path, rep, sdsbool):
        self.path = path         
        self.rep = rep
        self.bool = sdsbool 
        self.styleSheet = getSampleStyleSheet()
        self.elements = []

        self.blue = Color((32.0/255), (107.0/255), (196.0/255), 1)

        self.firstPage()
        self.nextPagesHeader(True)
        if sdsbool:
            self.sdsmaker()
        else: 
            self.escmaker()
        self.nextPagesHeader(False)        
        # Build
        self.doc = SimpleDocTemplate(path, pagesize=LETTER)
        self.doc.multiBuild(self.elements, canvasmaker=FooterCanvas)

    def firstPage(self):
        img = Image('static/lr.png', kind='proportional')
        img.drawHeight = 1.5*inch
        img.drawWidth = 2.4*inch
        img.hAlign = 'LEFT'
        self.elements.append(img)

        spacer = Spacer(0, 50)
        self.elements.append(spacer)

        img = Image('static/ohka.png')
        img.drawHeight = 3*inch
        img.drawWidth = 4*inch
        self.elements.append(img)

        spacer = Spacer(100, 200)
        self.elements.append(spacer)
        today = date.today()

        psDetalle = ParagraphStyle('Resumen', fontSize=9, leading=14, justifyBreaks=1, alignment=TA_LEFT, justifyLastLine=1)
        if self.bool:
            text = """Summary Data Sheet<br/>
            To be submitted to the EU's database<br/>"""
            
        else:
            text = """External Scorecard<br/>
            To be published to external stakeholders<br/>"""

        text += """System:  """+ str(self.rep.project.first().name) +"""<br/>
            Date: """+ str(today)

        paragraphReportSummary = Paragraph(text, psDetalle)
        self.elements.append(paragraphReportSummary)
        self.elements.append(PageBreak())

    def nextPagesHeader(self, isSecondPage):
        if isSecondPage:
            psHeaderText = ParagraphStyle('Hed0', fontSize=16, alignment=TA_LEFT, borderWidth=3, textColor=self.blue, fontName='Helvetica-Bold')
            if self.bool:
                text = 'Summary Data Sheet - ' + self.rep.project.first().name
            else:
                text = 'External Scorecard - ' + self.rep.project.first().name

            paragraphReportHeader = Paragraph(text, psHeaderText)
            self.elements.append(paragraphReportHeader)

            spacer = Spacer(10, 10)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.blue
            line.strokeWidth = 2
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 1)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.blue
            line.strokeWidth = 0.5
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 22)
            self.elements.append(spacer)

    def sdsmaker(self):   
        with open('yaml/sds/sds.yaml', 'r') as file:
            descriptions = yaml.load(file, Loader=yaml.FullLoader)
        for question in self.rep.questions.all():   
            psHeaderText = ParagraphStyle(
                'Hed0',
                fontSize=12,
                alignment=TA_LEFT,
                borderWidth=3,
                textColor=self.blue,
                fontName='Helvetica-Bold'  
            )
            text = str(question.number) + '. ' + descriptions.get(question.number, {}).get('title', '')
            paragraphReportHeader = Paragraph(text, psHeaderText)
            self.elements.append(paragraphReportHeader)

            spacer = Spacer(5, 5)
            self.elements.append(spacer)

            psHeaderText = ParagraphStyle('Hed0', fontSize=8, alignment=TA_LEFT, borderWidth=3,fontName='Helvetica-Bold' )
            text = descriptions.get(question.number, {}).get('text', '')
            paragraphReportHeader = Paragraph(text, psHeaderText)
            self.elements.append(paragraphReportHeader)

            spacer = Spacer(10, 10)
            self.elements.append(spacer)

            psHeaderText = ParagraphStyle('Hed0', fontSize=8, alignment=TA_LEFT, borderWidth=3,)
            text = str(question.answer)
            paragraphReportHeader = Paragraph(text, psHeaderText)
            self.elements.append(paragraphReportHeader)

            spacer = Spacer(10, 22)
            self.elements.append(spacer)

    def escmaker(self):           

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textData = ["1. Purpose","", "2. Values"]
                
        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)        

        data = [d]
        formattedLineData = []
        lineData = [self.rep.questions.filter(number=1).first().answer,"", self.rep.questions.filter(number=2).first().answer]
        print(lineData)

        styles = getSampleStyleSheet()
        style = styles['Normal']
        
        for item in lineData:
            paragraph = Paragraph(item.replace('\r\n', '<br/>'), style)
            formattedLineData.append(paragraph)
        data.append(formattedLineData)
        formattedLineData = []
        lineData = [ "","", ""]
        for item in lineData:
            ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
            p = Paragraph(ptext, centered)
            formattedLineData.append(p)
        data.append(formattedLineData)

        #print(data)
        table = Table(data, colWidths=[200, 50, 200])
        tStyle = TableStyle([
            # ('LINEABOVE', (0, 0), (-1, -1), 1, self.blue),
             ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (0, 0), self.blue),
            ('BACKGROUND', (2, 0), (2, 0), self.blue),
            ('LINEBEFORE', (0, 0), (-1, 1), 0, self.blue),
            ('LINEAFTER', (0, 0), (-1, 1), 0, self.blue),
            ('LINEBELOW', (0, 1), (0, 1), 0, self.blue),
            ('LINEBELOW', (2, 1), (2, 1), 0, self.blue)
        ])
            
        table.setStyle(tStyle)
        self.elements.append(table)

        styles = getSampleStyleSheet()

        d = []
        textData = textData = ["3. Data","", "4. Governance"]
                
        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)        

        data = [d]
        formattedLineData = []
        datatext = str(self.rep.questions.filter(number=3).first().answer) + '\r\n\r\n' \
            + str(self.rep.questions.filter(number=4).first().answer) + '\r\n\r\n' \
            + str(self.rep.questions.filter(number=5).first().answer) + '\r\n\r\n' \
            + str(self.rep.questions.filter(number=6).first().answer)
        datatext2 = str(self.rep.questions.filter(number=7).first().answer) + '\r\n\r\n' \
            + str(self.rep.questions.filter(number=8).first().answer) + '\r\n\r\n' \
            + str(self.rep.questions.filter(number=9).first().answer) + '\r\n\r\n' \
            + str(self.rep.questions.filter(number=10).first().answer)

        
        lineData = [datatext, "", datatext2 ]
        for item in lineData:
            paragraph = Paragraph(item.replace('\r\n', '<br/>'), style)
            formattedLineData.append(paragraph)
        data.append(formattedLineData)
        formattedLineData = []
        lineData = [ "","", ""]
        for item in lineData:
            ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
            p = Paragraph(ptext, centered)
            formattedLineData.append(p)
        data.append(formattedLineData)

        #print(data)
        table = Table(data, colWidths=[200, 50, 200])
        tStyle = TableStyle([
            # ('LINEABOVE', (0, 0), (-1, -1), 1, self.blue),
             ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (0, 0), self.blue),
            ('BACKGROUND', (2, 0), (2, 0), self.blue),
            ('LINEBEFORE', (0, 0), (-1, 1), 0, self.blue),
            ('LINEAFTER', (0, 0), (-1, 1), 0, self.blue),
            ('LINEBELOW', (0, 1), (0, 1), 0, self.blue),
            ('LINEBELOW', (2, 1), (2, 1), 0, self.blue)
        ])
            
        table.setStyle(tStyle)
        self.elements.append(table)


        

    
    
@login_required(login_url='signin')
def sds_pdf(request, pk):
    rep = get_object_or_404(SDS, pk=pk)
    report = PDFPSReporte('psreport.pdf', rep, True)
    # Assuming the script generates a PDF file named 'output.pdf'
    pdf_path = 'psreport.pdf'

    # Open the PDF file and read its contents
    with open(pdf_path, 'rb') as file:
        pdf_data = file.read()

    # Create a response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'
    response.write(pdf_data)

    return response

@login_required(login_url='signin')
def esc_pdf(request, pk):
    rep = get_object_or_404(ESC, pk=pk)
    print (rep.project.first().name)
    report = PDFPSReporte('psreport.pdf', rep, False)
    # Assuming the script generates a PDF file named 'output.pdf'
    pdf_path = 'psreport.pdf'

    # Open the PDF file and read its contents
    with open(pdf_path, 'rb') as file:
        pdf_data = file.read()

    # Create a response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'
    response.write(pdf_data)

    return response







    