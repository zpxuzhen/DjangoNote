from django.shortcuts import render
from django.shortcuts import render_to_response
from HelloWorld.forms import ContactForm
from django.http import Http404, HttpResponse
import datetime
from django.template import TemplateDoesNotExist
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from TestModel.models import Publisher
from django.views.generic import DetailView
from django.utils import timezone
from django.http import StreamingHttpResponse
import csv
from django.template import loader
from reportlab.pdfgen import canvas
from io import BytesIO



def hello(request):
    #context          = {}
    #context['hello'] = 'Hello World!'
    #return render(request, 'hello.html', context)
    return render_to_response('hello.html', {'hello': 'Hello World!'})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # 这里我们简单的把验证成功的数据显示到之前写的hello页面
            return render(request, "hello.html", {'hello': cd})
    else:
        form = ContactForm(
            initial={'subject': 'I love your site!'}
        )
    return render(request, "contact_form.html", {'form': form})

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def foobar_view(request):
    return render_to_response(template_name, {'hello': 'Hello World!'})
    
def object_list(request, model):
    obj_list = model.objects.all()
    template_name = '%s_list.html' % model.__name__.lower()
    return render_to_response(template_name, {'object_list': obj_list})

class AboutView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.template_name="about/%s.html" % context['page']
        return context

class PublisherList(ListView):
    model = Publisher
    context_object_name = 'my_favorite_publishers'

class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'publisher_list.html'
    def get_object(self):
        object = super().get_object()
        object.country = timezone.now()
        object.save()
        return object



def some_csv_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=some_csv.csv'

    # Create the CSV writer using the HttpResponse as the "file."
    writer = csv.writer(response)
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    for row in rows : writer.writerow(row) 

    return response


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="some_streaming_csv.csv"'
    return response


def some_template_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="some_template.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))

    t = loader.get_template('my_template_name.txt')
    response.write(t.render({'data': rows,}))
    return response
    

def some_pdf_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="some_pdf.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

    
def some_pdf2_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="some_pdf2.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


