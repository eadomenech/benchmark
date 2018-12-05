from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, FormView, UpdateView)

from .models import (
    Watermarking, CoverImage, WatermarkImage, Metric, Noise,
    SprintWatermarking, MetricSprintWatermarking, NoiseSprintWatermarking,
    MetricNoiseSprintWatermarking, ImageType)

from .forms import (
    WatermarkingForm, CoverImageForm, WatermarkImageForm, MetricForm,
    NoiseForm, ImageTypeForm)

from .task import mainTask


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
            mainTask.delay()
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
            mainTask.delay()
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
            mainTask.delay()
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
            mainTask.delay()
            return super(CreateMetric, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)
        return super(CreateMetric, self).form_invalid(form)


# Noise Views
class ListNoise(ListView):
    template_name = 'watermarking/lists/list_Noise.html'

    def get_queryset(self):
        """Return noises."""
        return Noise.objects.all()


class DetailNoise(DetailView):
    model = Noise
    template_name = 'watermarking/details/detail_Noise.html'


class CreateNoise(FormActionMixin, CreateView):

    model = Noise
    template_name = "watermarking/create/create_Noise.html"
    success_url = reverse_lazy("watermarking:noises")
    form_class = NoiseForm

    def form_valid(self, form):
        noise = form.save(commit=False)
        try:
            noise.save()
            mainTask.delay()
            return super(CreateNoise, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)
        return super(CreateNoise, self).form_invalid(form)


# Sprint Watermarking Views
class ListSprintWatermarking(ListView):
    template_name = 'watermarking/lists/list_SprintWatermarking.html'

    def get_queryset(self):
        """Return sprints."""
        return SprintWatermarking.objects.all()


# Metric Sprint Watermarking Views
class ListMetricSprintWatermarking(ListView):
    template_name = 'watermarking/lists/list_MetricSprintWatermarking.html'

    def get_queryset(self):
        """Return metric sprint."""
        return MetricSprintWatermarking.objects.all().order_by(
            'metric', '-value')


# Metric Sprint Watermarking Views
class ListNoiseSprintWatermarking(ListView):
    template_name = 'watermarking/lists/list_NoiseSprintWatermarking.html'

    def get_queryset(self):
        """Return noised sprint."""
        return NoiseSprintWatermarking.objects.all().order_by(
            'sprintWatermarking')


# Metric Noise Sprint Watermarking Views
class ListMetricNoiseSprintWatermarking(ListNoiseSprintWatermarking):
    template_name = 'watermarking/lists/list_MetricNoiseSprintWatermarking.html'


# Image Type Views
class ListImageType(ListView):
    template_name = 'watermarking/lists/list_ImageType.html'

    def get_queryset(self):
        """Return image types."""
        return ImageType.objects.all()


class CreateImageType(FormActionMixin, CreateView):

    model = ImageType
    template_name = "watermarking/create/create_ImageType.html"
    success_url = reverse_lazy("watermarking:imageTypes")
    form_class = ImageTypeForm

    def form_valid(self, form):
        imageType = form.save(commit=False)
        try:
            imageType.save()
            return super(CreateImageType, self).form_valid(form)
        except Exception as e:
            form.add_error(None, e)
        return super(CreateImageType, self).form_invalid(form)
