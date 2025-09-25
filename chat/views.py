import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from chat.models import Chat
from chat.forms import MessageForm


def home(request):
    context = {}
    return render(request, "base.html", context)


class UserDetailView(DetailView):
    model = User
    template_name = "chat/profile.html"


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        message = data.get('message')
        chat_uuid = data.get('chat_uuid')

        chat = get_object_or_404(Chat, chat_uuid=chat_uuid)
        
        # Sua lógica para salvar a mensagem
        # ...
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def chat_view(request, chat_uuid):
    chat = get_object_or_404(Chat, chat_uuid=chat_uuid)
    chat_messages = chat.messages.all()[:30] #type: ignore
    # form = MessageForm()

    other_user = None
    if chat.is_private:
        if request.user not in chat.users.all():
            raise Http404("Você não tem permissão para acessar este chat.")
        for user in chat.users.all():
            if user != request.user:
                other_user = user
                break
    
    # if request.method == "POST":
    #     data = json.loads(request.body)
    #     message = data.get('message')
    #     message.author = request.user
    #     message.group = chat
    #     message.save()
    #     context = {
    #         'message' : message,
    #         'user' : request.user
    #     }
    #     return render(request, 'chat/partials/chat_message_p.html', context)

    context = {
        'chat' : chat,
        'chat_messages' : chat_messages, 
        'chat_uuid' : chat.chat_uuid,
        # 'form' : form,
        'other_user' : other_user,
    }
    
    print(f"Accessing chat with UUID: {chat_uuid}")
    return render(request, 'chat/chat.html', context)


@login_required
def get_or_create_chat(request, username):
    # Caso usuário tente iniciar chat com ele mesmo, redireciona para home
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username = username)
    my_chatrooms = request.user.chats.filter(is_private = True)
    
    if my_chatrooms.exists():
        for chat in my_chatrooms:
            if other_user in chat.users.all():
                chatroom = chat
                break
            else:
                chatroom = Chat.objects.create(is_private = True)
                chatroom.users.add(other_user, request.user)
    else:
        chatroom = Chat.objects.create(is_private = True)
        chatroom.users.add(other_user, request.user)
        
    return redirect('chat', chatroom.chat_uuid)
