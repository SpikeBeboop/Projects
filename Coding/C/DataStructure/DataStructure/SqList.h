#pragma once
#include <string.h>

#define OK 1
#define ERROR 0
typedef int Status;

#define MAXSIZE 20		/*�洢�ռ��ʼ������*/
typedef int ElemType;	/*ElemType���͸���ʵ�����������������int*/
typedef struct
{
	ElemType data[MAXSIZE];	/*���飬 �洢����Ԫ��*/
	int length;				/*���Ա�ǰ����*/
}SqList;

// ��ʼ������
Status InitList(SqList* L);

//�����Ƿ�Ϊ��
Status ListEmpty(SqList L);

//�����Ա����
Status ClearList(SqList* L);

//�����Ա�L�е�i��Ԫ�ط��ظ�e
Status GetElem(SqList L, int i, ElemType* e);

