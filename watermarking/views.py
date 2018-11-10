from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, FormView, UpdateView)

from .models import Watermarking, CoverImage, WatermarkImage, Metric
from .forms import (
    WatermarkingForm, CoverImageForm, WatermarkImageForm, MetricForm)

from .task import my_first_task


def index(request):
    my_first_task.delay(100)
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


class CreateCoverImage(FormActionMixin, CreateView):

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


class CreateWatermarkImage(FormActionMixin, CreateView):

    model = WatermarkImage
    template_name = "watermarking/create/create_WatermarkImage.html"
    success_url = reverse_lazy("watermarking:watermarkImages")
    form_class = WatermarkImageForm

    def form_valid(self, form):
        coverImage = form.save(commit=False)
        try:
            coverImage.save()
            return super(CreateWatermarkImage, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)

        return super(CreateWatermarkImage, self).form_invalid(form)


# Metrics Views
class ListMetric(ListView):
    template_name = 'watermarking/lists/list_Metric.html'

    def get_queryset(self):
        """Return metrics."""
        return Metric.objects.all()


class DetailMetric(DetailView):
    model = Metric
    template_name = 'watermarking/details/detail_Metric.html'


class CreateMetric(FormActionMixin, CreateView):

    model = Metric
    template_name = "watermarking/create/create_Metric.html"
    success_url = reverse_lazy("watermarking:metrics")
    form_class = MetricForm

    def form_valid(self, form):
        metric = form.save(commit=False)
        try:
            metric.save()
            return super(CreateMetric, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)
        return super(CreateMetric, self).form_invalid(form)
