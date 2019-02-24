from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from default.models import Question, Reply, Comment, Agree, Favorite, Follow, ImageStore, UserProfile


def signout(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup(request):
    if (request.method == "GET"):
        return render(request, 'signup.html', {'msg': ""})
    elif (request.method == "POST"):
        username = request.POST['username']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            password = request.POST['password']
            User.objects.create_user(username=username, password=password)
            return render(request, 'signup.html', {'msg': "Success"})
        return render(request, 'signup.html', {'msg': "AlreadyExist"})


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {'msg': ""})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # return render(request, 'index.html', {})
                return HttpResponseRedirect("/")
            else:
                return render(request, 'signin.html', {'msg': "用户名或密码错误"})
        else:
            return render(request, 'signin.html', {'msg': "用户名或密码错误"})


def index(request):
    all = Question.objects.all().order_by("addtime").reverse()
    hot = Question.objects.all().order_by("hitcount").reverse()
    question = {"all": all, "hot": hot}
    if "search" in request.POST:
        str_search = request.POST["search"]
        question["all"] = Question.objects.filter(title__contains=str_search) | \
                          Question.objects.filter(description__contains=str_search)
        question["hot"] = Question.objects.all().order_by("hitcount").reverse()

    try:
        current_user = User.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        return render(request, 'index.html', {'question': question})

    # current_user = User.objects.get(id=request.user.id)
    count = 0
    if not Reply.objects.filter(isread=False).count() == 0:
        for i in Reply.objects.filter(isread=False):
            if i.question.author == current_user:
                count += 1
    reply_msg = count
    follow_msg = Follow.objects.filter(isread=False, followb=current_user).count()
    count = 0
    if Favorite.objects.filter(isread=False).count() != 0:
        for i in Favorite.objects.filter(isread=False):
            if i.question.author == current_user:
                count += 1
    fav_msg = count
    count = 0
    if Agree.objects.filter(isread=False).count() != 0:
        for i in Agree.objects.filter(isread=False):
            if i.reply.author == current_user:
                count += 1
    agree_msg = count
    user_msg = {"reply_msg": reply_msg, "follow_msg": follow_msg, "fav_msg": fav_msg, "agree_msg": agree_msg}

    question_info = Question.objects.filter(author=current_user).count()
    reply_info = Reply.objects.filter(author=current_user).count()
    follow_info = Follow.objects.filter(afollow=current_user).count()
    fav_info = Favorite.objects.filter(author=current_user).count()
    agree_info = Agree.objects.filter(author=current_user).count()
    user_info = {"question_info": question_info, "reply_info": reply_info, "follow_info": follow_info,
                 "fav_info": fav_info, "agree_info": agree_info}

    try:
        user_portrait =UserProfile.objects.get(user=request.user).portrait
    except ObjectDoesNotExist:
        user_portrait=None

    if (request.method == "GET"):
        return render(request, 'index.html', {'question': question, 'user_msg': user_msg, 'user_info': user_info, 'user_portrait': user_portrait})
    elif (request.method == "POST"):
        if "title" in request.POST:
            title = request.POST['title']
            if "description" in request.POST:
                description = request.POST['description']
                user = request.user
                Question.objects.create(author=user, title=title, description=description)
        if "search" in request.POST:
            str_search = request.POST["search"]
            question["all"] = Question.objects.filter(title__contains=str_search) | \
                              Question.objects.filter(description__contains=str_search)
            question["hot"] = question["all"].hot = Question.objects.all().order_by("hitcount").reverse()
    return render(request, 'index.html', {'question': question, 'user_msg': user_msg, 'user_info': user_info, 'user_portrait': user_portrait})


def hottopic(request):
    return HttpResponse("hottopic")


def setting(request):
    return HttpResponse("setting")


def home(request):
    return render(request, 'home/base_home.html', {})


def follow(request):
    afollow = User.objects.get(id=request.user.id)
    followb = User.objects.get(id=request.GET["follow_id"])
    if afollow == followb:
        return HttpResponse("")
    exist = True
    try:
        Follow.objects.get(afollow=afollow, followb=followb)
    except ObjectDoesNotExist:
        exist = False
    if "load" in request.GET:
        if request.GET['load'] == "1":
            if exist:
                return HttpResponse("取消关注")
            else:
                return HttpResponse("关注")
    elif "update" in request.GET:
        if request.GET["update"] == "1":
            if exist:
                Follow.objects.get(afollow=afollow, followb=followb).delete()
                return HttpResponse("关注")
            else:
                Follow.objects.create(afollow=afollow, followb=followb)
                return HttpResponse("取消关注")
    return HttpResponse("hello")


def question(request):
    question_id = request.GET["question_id"]
    question = Question.objects.get(id=question_id)
    question.hitcount += 1
    question.save()
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)

    if (request.method == "POST"):
        # if "reply_content" in request.POST:
        reply_content = request.POST["reply_content"]
        if "img" in request.FILES:
            new_img = ImageStore(
                img=request.FILES.get('img'),
                name=request.FILES.get('img').name
            )
            new_img.save()
            Reply.objects.create(author=current_user, question=question, content=reply_content, picture=new_img)
        else:
            Reply.objects.create(author=current_user, question=question, content=reply_content)

    reply = Reply.objects.filter(question_id=question_id).order_by("addtime").reverse()
    return render(request, 'question.html', {"question": question, "reply": reply})


# def comment(request):


def reply(request):
    pass


def favorite(request):
    user = User.objects.get(id=request.user.id)
    question = Question.objects.get(id=request.GET["question_id"])
    exist = True
    try:
        Favorite.objects.get(author=user, question=question)
    except ObjectDoesNotExist:
        exist = False
    if "load" in request.GET:
        if request.GET['load'] == "1":
            if exist:
                return HttpResponse("取消收藏")
            else:
                return HttpResponse("收藏")
    elif "update" in request.GET:
        if request.GET["update"] == "1":
            if exist:
                Favorite.objects.get(author=user, question=question).delete()
                return HttpResponse("收藏")
            else:
                Favorite.objects.create(author=user, question=question)
                return HttpResponse("取消收藏")
    return HttpResponse("hello")


def agree(request):
    user = User.objects.get(id=request.user.id)
    reply = Reply.objects.get(id=request.GET["reply_id"])
    exist = True
    try:
        Agree.objects.get(author=user, reply=reply)
    except ObjectDoesNotExist:
        exist = False
    if "load" in request.GET:
        if request.GET['load'] == "1":
            if exist:
                return HttpResponse("取消赞")
            else:
                return HttpResponse("点赞")
    elif "update" in request.GET:
        if request.GET["update"] == "1":
            if exist:
                Agree.objects.get(author=user, reply=reply).delete()
                return HttpResponse("点赞")
            else:
                Agree.objects.create(author=user, reply=reply)
                return HttpResponse("取消赞")
    return HttpResponse("hello")


def uploadImg(request):
    if request.method == 'POST':
        new_img = ImageStore(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
        try:
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.portrait=new_img
            userprofile.save()
            # userprofile(portrait_id=new_img.id)
            # userprofile.__setattr__("portrait_id",new_img.id)
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=request.user,portrait=new_img)
    return render(request, 'uploadimg.html')


def showImg(request):
    imgs = ImageStore.objects.all()
    content = {
        'imgs': imgs,
    }
    for i in imgs:
        print(i.img.url)

    return render(request, 'showimg.html', content)


def get_this_user_msg(request):
    try:
        this_user = User.objects.get(id=request.GET["user_id"])
    except ObjectDoesNotExist:
        return render(request, 'index.html', {})

    try:
        portrait =UserProfile.objects.get(user=this_user).portrait
    except ObjectDoesNotExist:
        portrait=None

    follow_msg_all_list = Follow.objects.filter(followb=this_user)
    follow_msg_read_list = follow_msg_all_list.filter(isread=True)
    follow_msg_unread_list = follow_msg_all_list.filter(isread=False)
    follow_msg_dic = {"list": {"read": follow_msg_read_list, "unread": follow_msg_unread_list,
                               "all": follow_msg_all_list},
                      "count": {"read": follow_msg_read_list.count(), "unread": follow_msg_unread_list.count(),
                                "all": follow_msg_all_list.count()}}

    reply_msg_all_list = Reply.objects.filter(id=0)
    for q in Question.objects.filter(author=this_user):
        reply_msg_all_list = reply_msg_all_list | q.reply_set.all()
    reply_msg_read_list = reply_msg_all_list.filter(isread=True)
    reply_msg_unread_list = reply_msg_all_list.filter(isread=False)
    reply_msg_dic = {"list": {"read": reply_msg_read_list, "unread": reply_msg_unread_list,
                              "all": reply_msg_all_list},
                     "count": {"read": reply_msg_read_list.count(), "unread": reply_msg_unread_list.count(),
                               "all": reply_msg_all_list.count()}}

    fav_msg_all_list = Favorite.objects.filter(id=0)
    for q in Question.objects.filter(author=this_user):
        fav_msg_all_list = fav_msg_all_list | q.favorite_set.all()
    fav_msg_read_list = fav_msg_all_list.filter(isread=True)
    fav_msg_unread_list = fav_msg_all_list.filter(isread=False)
    fav_msg_dic = {"list": {"read": fav_msg_read_list, "unread": fav_msg_unread_list,
                            "all": fav_msg_all_list},
                   "count": {"read": fav_msg_read_list.count(), "unread": fav_msg_unread_list.count(),
                             "all": fav_msg_all_list.count()}}

    agree_msg_all_list = Agree.objects.filter(id=0)
    for q in Reply.objects.filter(author=this_user):
        agree_msg_all_list = agree_msg_all_list | q.agree_set.all()
    agree_msg_read_list = agree_msg_all_list.filter(isread=True)
    agree_msg_unread_list = agree_msg_all_list.filter(isread=False)
    agree_msg_dic = {"list": {"read": agree_msg_read_list, "unread": agree_msg_unread_list,
                              "all": agree_msg_all_list},
                     "count": {"read": agree_msg_read_list.count(), "unread": agree_msg_unread_list.count(),
                               "all": agree_msg_all_list.count()}}

    this_user_msg = {"id": this_user.id, "username": this_user.username,"portrait":portrait,
                     "reply_msg": reply_msg_dic, "follow_msg": follow_msg_dic,
                     "fav_msg": fav_msg_dic, "agree_msg": agree_msg_dic, }
    return this_user_msg


def question_info(request):
    this_user_msg = get_this_user_msg(request)
    question_info_list = Question.objects.filter(author_id=this_user_msg["id"])
    question_info = {"list": question_info_list, "count": question_info_list.count()}
    return render(request, 'home/info/question.html', {"this_user": this_user_msg, "question": question_info})


def reply_info(request):
    this_user_msg = get_this_user_msg(request)
    reply_info_list = Reply.objects.filter(author_id=this_user_msg["id"])
    reply_info = {"list": reply_info_list, "count": reply_info_list.count()}
    return render(request, 'home/info/reply.html', {"this_user": this_user_msg, "reply": reply_info})


def follow_info(request):
    this_user_msg = get_this_user_msg(request)
    follow_info_list = Follow.objects.filter(afollow_id=this_user_msg["id"])
    follow_info = {"list": follow_info_list, "count": follow_info_list.count()}
    return render(request, 'home/info/follow.html', {"this_user": this_user_msg, "follow": follow_info})


def fav_info(request):
    this_user_msg = get_this_user_msg(request)
    fav_info_list = Favorite.objects.filter(author_id=this_user_msg["id"])
    fav_info = {"list": fav_info_list, "count": fav_info_list.count()}
    return render(request, 'home/info/favorite.html', {"this_user": this_user_msg, "favorite": fav_info})


def agree_info(request):
    this_user_msg = get_this_user_msg(request)
    agree_info_list = Agree.objects.filter(author_id=this_user_msg["id"])
    agree_info = {"list": agree_info_list, "count": agree_info_list.count()}
    return render(request, 'home/info/agree.html', {"this_user": this_user_msg, "agree": agree_info})


def reply_msg(request):
    this_user_msg = get_this_user_msg(request)
    list = this_user_msg["reply_msg"]["list"]["unread"]
    for i in list:
        i.__setattr__("isread", True)
        i.save()
    return render(request, 'home/msg/reply.html', {"this_user": this_user_msg})


def follow_msg(request):
    this_user_msg = get_this_user_msg(request)
    list = this_user_msg["follow_msg"]["list"]["unread"]
    for i in list:
        i.__setattr__("isread", True)
        i.save()
    return render(request, 'home/msg/follow.html', {"this_user": this_user_msg})


def fav_msg(request):
    this_user_msg = get_this_user_msg(request)
    list = this_user_msg["fav_msg"]["list"]["unread"]
    for i in list:
        i.__setattr__("isread", True)
        i.save()
    return render(request, 'home/msg/favorite.html', {"this_user": this_user_msg})


def agree_msg(request):
    this_user_msg = get_this_user_msg(request)
    list = this_user_msg["agree_msg"]["list"]["unread"]
    for i in list:
        i.__setattr__("isread", True)
        i.save()
    return render(request, 'home/msg/agree.html', {"this_user": this_user_msg})
