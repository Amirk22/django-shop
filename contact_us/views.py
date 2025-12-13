from django.shortcuts import render , reverse ,redirect
from django.views import View
from .forms import ContactForm
from rest_framework.generics import ListCreateAPIView

from .models import Contact
from .serializers import ContactSerializer


# Create your views here.



class ContactUSView(View):
    def get(self, request):
        form = ContactForm()
        return render(request,'contact_us/contact_us.html',{'contact_form':form})
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')
        return render(request,'contact_us/contact_us.html',{'contact_form':form})


#....................................................API

class ContactUsAPIView(ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

