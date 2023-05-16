from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import yaml

from sds.models import Template, TempQuestion, SDS
from projects.models import Project 
import subprocess

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color
    
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
        self.drawImage("static/ohka.png", self.width - inch * 2, self.height-50, width=100, height=30, preserveAspectRatio=True, mask='auto')
        self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Times-Roman', 10)
        self.drawString(LETTER[0]-x, 65, page)
        self.restoreState()

class PDFPSReporte:

    def __init__(self, path, sds):
        self.path = path
        self.sds = sds
        self.styleSheet = getSampleStyleSheet()
        self.elements = []

        self.blue = Color((32.0/255), (107.0/255), (196.0/255), 1)

        self.firstPage()
        self.nextPagesHeader(True)
        self.sdsmaker()
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

        spacer = Spacer(30, 100)
        self.elements.append(spacer)

        img = Image('static/ohka.png')
        img.drawHeight = 1.5*inch
        img.drawWidth = 5.5*inch
        self.elements.append(img)

        spacer = Spacer(10, 250)
        self.elements.append(spacer)
        today = date.today()

        psDetalle = ParagraphStyle('Resumen', fontSize=9, leading=14, justifyBreaks=1, alignment=TA_LEFT, justifyLastLine=1)
        text = """Summary Data Sheet<br/>
        To be submitted to the EU's database<br/>
        System:  """+ str(self.sds.project.first().name) +"""<br/>
        Date: """+ str(today)
        paragraphReportSummary = Paragraph(text, psDetalle)
        self.elements.append(paragraphReportSummary)
        self.elements.append(PageBreak())

    def nextPagesHeader(self, isSecondPage):
        if isSecondPage:
            psHeaderText = ParagraphStyle('Hed0', fontSize=16, alignment=TA_LEFT, borderWidth=3, textColor=self.blue, fontName='Helvetica-Bold')
            text = 'Summary Data Sheet - ' + self.sds.project.first().name
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
        for question in self.sds.questions.all():   
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

        

    
    
# # Create your views here.
@login_required(login_url='signin')
def sds_pdf(request, pk):
    sds = get_object_or_404(SDS, pk=pk)
    print (sds.project.first().name)
    report = PDFPSReporte('psreport.pdf', sds)
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







    