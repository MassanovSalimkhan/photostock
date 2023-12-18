from django.shortcuts import get_object_or_404

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from .models import Photo

from django.http import HttpResponse


class PhotoListView(ListView):

    model = Photo     

    template_name = 'photoapp/list.html'

    context_object_name = 'photo'


# class PhotoTagListView(PhotoListView):

#     template_name = 'photoapp/taglist.html'

#     def get_tag(self):
#         return self.kwargs.get('tag')

#     def get_queryset(self):
#         return self.model.objects.filter(tags__slug=self.get_tag())

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tag"] = self.get_tag()
#         return context
    

class PhotoDetailView(DetailView):

    model = Photo

    template_name = 'photoapp/detail.html'

    context_object_name = 'photo'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        submitter_photo_count = Photo.objects.filter(submitter=self.object.submitter).count()
        context['submitter_photo_count'] = submitter_photo_count

        return context






class PhotoCreateView(LoginRequiredMixin, CreateView):

    model = Photo

    fields = ['title', 'description', 'image']

    template_name = 'photoapp/create.html'

    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):

        form.instance.submitter = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):

    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')
        

class PhotoUpdateView(UserIsSubmitter, UpdateView):

    template_name = 'photoapp/update.html'

    model = Photo

    fields = ['title', 'description']

    success_url = reverse_lazy('photo:list')



class PhotoDeleteView(UserIsSubmitter, DeleteView):

    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:list')  



class PhotoDownloadView(UserPassesTestMixin, View):
    
    def test_func(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        return self.request.user == photo.submitter or self.request.user.groups.filter(name='AuthorizedUsers').exists()

    def handle_no_permission(self):
        return HttpResponse("You are not authorized to download the full-size image.", status=403)

    def download_full_size(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])

        
        if not self.test_func():
            return self.handle_no_permission()
        

        if not self.test_func():
            return self.handle_no_permission()


        response = HttpResponse(photo.image.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{photo.title}.jpg"'
        return response
    

    


        
    def download_thumbnail(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])

        response = HttpResponse(photo.image_thumbnail.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{photo.title}_thumbnail.jpg"'
        return response
    
    def get(self, request, *args, **kwargs):
        if 'thumbnail' in request.GET:
            return self.download_thumbnail(request, *args, **kwargs)
        else:
            return self.download_full_size(request, *args, **kwargs)