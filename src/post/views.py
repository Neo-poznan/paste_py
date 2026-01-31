import json

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from post.models import Posts
from post.infrastructure.code_executor import execute_code
from asgiref.sync import sync_to_async
from post.services.post_service import create_post, get_post, remove_unnecessary_line_breaks


class CreateNewPostView(View):
    template_name = 'post/index.html'
    
    async def get(self, request):  
        'When the user accesses the main page, display the form to create a new post'
        return render(self.request, self.template_name)

    async def post(self, request):
        '''
        When the user submits the form, accept it in JSON format,
        request a key for it, save deletion and view data in the DB,
        and save the text in S3 storage, then send the link back to the user
        '''
        body_unicode = request.body.decode('utf-8')
        form_data = json.loads(body_unicode)
        post_content = form_data['text']
        expire_date = form_data['expire_date']
        post_url = await create_post(post_content, expire_date)
        return JsonResponse({'link': post_url})
    

async def execute_code_view(request):
    '''
    View for executing code sent in the request body.
    Expects a JSON payload with a 'text' field containing the code to execute.
    '''
    body_unicode = request.body.decode('utf-8')
    form_data = json.loads(body_unicode) 
    code = form_data['text']
    code = await remove_unnecessary_line_breaks(code)
    result = await execute_code(code)
    return JsonResponse(result)


async def get_post_view(request, post_key):
    '''
    If the post does not exist, display an appropriate message,
    if the post exists, display the post text and update the view count
    '''
    # if the user has not yet viewed this post, increase the view count
    is_viewed = await sync_to_async(request.session.get)(post_key)
    try:
        context = await get_post(post_key, need_update_views_count=not is_viewed)
    except Posts.DoesNotExist:
        return render(request, 'post/post.html', context={'post_content': 'Post not found or deleted!', 'views': 0})
    except Exception:
        return render(request, 'post/post.html', context={'post_content': 'Error loading content!', 'views': 0})
    if not is_viewed:
        await sync_to_async(request.session.__setitem__)(post_key, True)
    return render(request, 'post/post.html', context=context)

