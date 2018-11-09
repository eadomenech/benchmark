from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, FormView, UpdateView)

from .models import Watermarking, CoverImage, WatermarkImage
from .forms import WatermarkingForm, CoverImageForm, WatermarkImageForm


def index(request):
    return render(request, 'watermarking/index.html')


# Watermarking Views
class ListWatermarking(ListView):
    template_name = 'watermarking/lists/list_Watermarking.html'

    def get_queryset(self):
        """Return the watermarking methods."""
        return Watermarking.objects.all()


class DetailWatermarking(DetailView):
    model = Watermarking
    template_name = 'watermarking/details/detail_Watermarking.html'


class FormActionMixin(object):

    def post(self, request, *args, **kwargs):
        """Add 'Cancel' button redirect."""
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(FormActionMixin, self).post(request, *args, **kwargs)


class CreateWatermarking(FormActionMixin, CreateView):

    model = Watermarking
    template_name = "watermarking/create/create_Watermarking.html"
    success_url = reverse_lazy("watermarking:methods")
    form_class = WatermarkingForm

    def form_valid(self, form):
        watermarking = form.save(commit=False)
        try:
            watermarking.save()
            return super(CreateWatermarking, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)

        return super(CreateWatermarking, self).form_invalid(form)


# Cover Image Views
class ListCoverImage(ListView):
    template_name = 'watermarking/lists/list_CoverImage.html'

    def get_queryset(self):
        """Return the watermarking methods."""
        return CoverImage.objects.all()


class DetailCoverImage(DetailView):
    model = CoverImage
    template_name = 'watermarking/details/detail_CoverImage.html'


class CreateCoverImage(CreateView):

    model = CoverImage
    template_name = "watermarking/create/create_CoverImage.html"
    success_url = reverse_lazy("watermarking:coverImages")
    form_class = CoverImageForm

    def form_valid(self, form):
        coverImage = form.save(commit=False)
        try:
            coverImage.save()
            return super(CreateCoverImage, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)

        return super(CreateCoverImage, self).form_invalid(form)


# Watermark Image Views
class ListWatermarkImage(ListView):
    template_name = 'watermarking/lists/list_WatermarkImage.html'

    def get_queryset(self):
        """Return the watermarking methods."""
        return WatermarkImage.objects.all()


class DetailWatermarkImage(DetailView):
    model = WatermarkImage
    template_name = 'watermarking/details/detail_WatermarkImage.html'


class CreateWatermarkImage(CreateView):

    model = WatermarkImage
    template_name = "watermarking/create/create_WatermarkImage.html"
    success_url = reverse_lazy("watermarking:coverImages")
    form_class = WatermarkImageForm

    def form_valid(self, form):
        coverImage = form.save(commit=False)
        try:
            coverImage.save()
            return super(CreateWatermarkImage, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)

        return super(CreateWatermarkImage, self).form_invalid(form)
