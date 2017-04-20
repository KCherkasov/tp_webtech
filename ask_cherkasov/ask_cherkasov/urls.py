from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from ask_cherkasov import views, settings

urlpatterns = [
  url(r'^admin/', admin.site.urls, name="admin"),
  url(r'^base/', views.base, name="base"),
  url(r'^$', views.newest, name="questions-new"),
  url(r'^hot/', views.hottest, name="questions-hot"),
  url(r'^tag/(?P<tag>.+)/', views.by_tag, name="tag"),
  url(r'^question/(?P<id>\d+)/', views.question, name="question"),
  url(r'^ask/', views.ask, name="ask"),
  url(r'^login/', views.login, name="sign-in"),
  url(r'^signup/', views.signup, name="sign-up"),
  url(r'^edit/', views.edit, name="profile-edit"),
  url(r'^hello_world/', views.hello_world, name="hello-world-sample"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
