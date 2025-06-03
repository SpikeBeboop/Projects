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

// 初始化操作，建立一个空的线性表L
Status InitList(SqlList* L);

// 判断线性表是否为空
Status ListEmpty(SqlList L);

//将线性表清空
Status ClearList(SqlList* L);

//将线性表L中第i个位置元素返回给e。
Status GetElem(SqlList L, int i, ElemType* e);

Status DestroyList