from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView

from chat.models import Chat


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    online_users = User.objects.filter(status__online_status=True)
    context = {'online_users': online_users}

    return render(request, 'chat/home.html', context)


@login_required
def chat_view(request, chat_uuid):
    chat = get_object_or_404(Chat, chat_uuid=chat_uuid)
    chat_messages = chat.messages.all()[:30] #type: ignore

    other_user = None
    if chat.is_private:
        if request.user not in chat.users.all():
            raise Http404("Você não tem permissão para acessar este chat.")
        for user in chat.users.all():
            if user != request.user:
                other_user = user
                break

    context = {
        'chat' : chat,
        'chat_messages' : chat_messages, 
        'chat_uuid' : chat.chat_uuid,
        'other_user' : other_user,
    }
    
    return render(request, 'chat/chat.html', context)


@login_required
def get_or_create_chat(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username = username)
    my_chatrooms = request.user.chats.all()
    
    for chat in my_chatrooms:
        print(chat.users.all())
        if other_user in chat.users.all():
            chatroom = chat
            print("Chatroom existente encontrado.")
            return redirect('chat', chatroom.chat_uuid)
        else:
            continue

    chatroom = Chat.objects.create(is_private = True)
    print("Novo chatroom criado com my_chatrooms vazio.")
    chatroom.users.add(other_user, request.user)

    return redirect('chat', chatroom.chat_uuid)


@login_required
def search_users(request):
    query = request.GET.get('username', '')
    users = User.objects.all()

    if query:
        user_list = users.filter(username__icontains=query)
        return render(
            request, 'chat/search.html',
            context = {'user_list': user_list }
        )
    
    return redirect('home')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "chat/profile.html"

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)
    