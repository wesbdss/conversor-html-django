from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django.template.loader import render_to_string, get_template, TemplateDoesNotExist
from django.conf import settings
from django.utils import timezone
import os, sys, platform
from . import models
from django.views.decorators.csrf import csrf_exempt
import shutil
# Create your views here.

path_root = os.path.join(settings.BASE_DIR,".templates")
new_directory = os.path.join(settings.BASE_DIR,"templates_generated")

def conversorView(request):
    print(">>","conversorView")
    metadata = {
        "created_at":timezone.now(),
        "source": "django_generator",
        "version": "beta",
    }
    ignore_files = ["assets",".gitignore","LICENSE","README.md",".git"]
    values = os.listdir(path_root)
    values = [path_root+v for v in values if v not in ignore_files]
    
    no_dirs = True
    while no_dirs:
        no_dirs = False
        diretory = None
        for v in values:
            if(os.path.isfile(v)):
                pass
            elif(os.path.isdir(v)):
                no_dirs = True
                diretory = v
                break
        if diretory:
            subfiles = os.listdir(diretory)
            if len(subfiles) == 0:
                values.pop(values.index(v))
            else:
                [values.append(diretory+"/"+f) for f in subfiles]
                values.pop(values.index(v))
                
    # Save Templates
    templates_dirs = [d.replace(path_root,new_directory) for d in values]
    for i,t in enumerate(templates_dirs):
        t_dir = "/".join(t.split("/")[:-1])
        t_name = t.replace(new_directory,"")
        os.makedirs(t_dir, exist_ok=True)
        template_rended = render_to_string(t_name,context={})
        with open(t, "w+") as f:
            f.write(template_rended)
            f.close()
    
    # generate meta
    with open(new_directory+"meta.json", "w+") as f:
        f.write(metadata)
        f.close()
    return HttpResponse("<br>".join(["<a href='/{}'>{}</a>".format(t.replace(new_directory,""),t.replace(new_directory,"")) for t in templates_dirs]))

def pageView(request):
    
    print(">>","pageView")
    print(request.build_absolute_uri(),os.path.join(path_root,request.path.lstrip('/')))
    print("__file__ ", __file__)
    print("path root", path_root)
    print("dirs", os.listdir(path_root))
    try:
        if os.path.isdir(os.path.join(path_root,request.path.lstrip('/'))) and os.path.exists(os.path.join(path_root,"index.html")):
            template = get_template(os.path.join(path_root,"index.html"))
            return HttpResponse(template.render({"request":request}))
        template = get_template(request.path.lstrip('/'))
        return HttpResponse(template.render({"request":request}))
    except Exception as ex:
        print("--- ERROR ---")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(request.path.lstrip('/'))
        print("Err:", ex)
        print("--- END ERROR ---")
        # Return first index.html

    if settings.DEBUG:
        if not os.path.isdir(str(path_root+request.path.lstrip('/'))) and not str(path_root+request.path.lstrip('/')).endswith(".html"):
            raise Http404("Não é um diretório {}".format(os.path.isdir(str(path_root+request.path.lstrip('/')))))
        values = os.listdir(str(path_root+request.path.lstrip('/')))
        return HttpResponse("<br>".join(["<a href='{}'>{}</a>".format((request.path+"/"+t).replace("//","/"),t) for t in values]))
    raise Http404("Template não Encontrado")
            
        