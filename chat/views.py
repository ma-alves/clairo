from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView

from chat.models import Chat
from chat.forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def home(request):
    context = {}
    return render(request, "base.html", context)


class UserDetailView(DetailView):
    model = User
    template_name = "chat/profile.html"


@login_required
def chat_view(request, chat_uuid):
    chat = get_object_or_404(Chat, chat_uuid=chat_uuid)
    chat_messages = chat.messages.all()[:30] #type: ignore
    form = MessageForm()

    other_user = None
    if chat.is_private:
        if request.user not in chat.users.all():
            raise Http404("Você não tem permissão para acessar este chat.")
        for user in chat.users.all():
            if user != request.user:
                other_user = user
                break
    
    if request.htmx:
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat
            message.save()
            context = {
                'message' : message,
                'user' : request.user
            }
            return render(request, 'chat/partials/chat_message_partial.html', context)
    
    context = {
        'chat_messages' : chat_messages, 
        'form' : form,
        'other_user' : other_user,
        'chat_uuid' : chat.chat_uuid,
    }
    
    return render(request, 'chat/chat.html', context)


@login_required
def get_or_create_chat(request, username):
    # Caso usuário tente iniciar chat com ele mesmo, redireciona para home
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username = username)
    my_chatrooms = request.user.chats.filter(is_private = True)
    
    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = Chat.objects.create(is_private = True)
                chatroom.users.add(other_user, request.user)
    else:
        chatroom = Chat.objects.create(is_private = True)
        chatroom.users.add(other_user, request.user)
        
    return redirect('chat', chatroom.chat_uuid)
