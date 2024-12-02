from django.shortcuts import render
from .models import Comment, Board
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .seralizers import BoardSeralizers, CommentSeralizers
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.http.response import JsonResponse
# Create your views here.


@api_view(['GET', 'POST'])
def boards(request):
    # 게시글 전체조회
    # 전체조회할때 Params 에 page=? 넘겨줘야함
    if request.method == 'GET':
        board = Board.objects.all()  # 게시글 전체 조회
        paginator = Paginator(board, 10)  # 한 페이지에 10개 게시글씩
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # 직렬화 및 페이징 처리된 데이터 반환
        serializers = BoardSeralizers(page_obj.object_list, many=True)
        return Response({
            'results': serializers.data,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        })
    
    # 게시글 생성하기
    elif request.method == 'POST':
        user = request.user
        serializers = BoardSeralizers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save(User=user)
            return Response(serializers.data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def boards_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # 게시판 글 디테일과 그 게시글의 댓글 전체조회
    # 여기도 마찬가지
    if request.method == 'GET':
        board_comment = board.comments.all()  # 해당 게시글의 댓글들
        paginator = Paginator(board_comment, 10)  # 한 페이지에 10개의 댓글씩
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(board_comment)
        if board_comment:
            seralizers = CommentSeralizers(page_obj.object_list, many=True)
        else:
            seralizers = BoardSeralizers(board)
        return Response({
            'results': seralizers.data,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        })
    
    # 댓글 생성하기
    elif request.method == 'POST':
        user = request.user
        seralizers = CommentSeralizers(data=request.data)
        if seralizers.is_valid(raise_exception=True):
            seralizers.save(board=board, User=user)
            return Response(seralizers.data)
        
    # 게시글 수정하기
    elif request.method == 'PUT':
        seralizers = BoardSeralizers(instance=board, data=request.data)
        if seralizers.is_valid(raise_exception=True):
            seralizers.save()
            return Response(seralizers.data, status=status.HTTP_202_ACCEPTED)

    # 게시글 삭제하기
    elif request.method == 'DELETE':
        pk = board.pk
        board.delete()
        return JsonResponse({'msg':f"{pk}번째 게시글 삭제 완료"})
    
@api_view(['DELETE'])
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return JsonResponse({'msg':f'{pk}번째 댓글 삭제 완료되었습니다.'})