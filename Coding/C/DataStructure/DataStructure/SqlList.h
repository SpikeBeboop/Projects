#pragma once
#include <stdlib.h>
#include <string.h>

#define MAXSIZE 20
#define TRUE 1
#define FALSE 0

typedef int ElemType;
typedef int Status;
typedef struct
{
	ElemType data[MAXSIZE];
	int length;
}SqlList;

// ��ʼ������������һ���յ����Ա�L
Status InitList(SqlList* L);

// �ж����Ա��Ƿ�Ϊ��
Status ListEmpty(SqlList L);

//�����Ա����
Status ClearList(SqlList* L);

//�����Ա�L�е�i��λ��Ԫ�ط��ظ�e��
Status GetElem(SqlList L, int i, ElemType* e);

Status DestroyList