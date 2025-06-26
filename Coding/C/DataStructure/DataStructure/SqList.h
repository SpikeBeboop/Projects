#pragma once
#include <string.h>

#define OK 1
#define ERROR 0
typedef int Status;

#define MAXSIZE 20		/*存储空间初始分配量*/
typedef int ElemType;	/*ElemType类型根据实际情况而定，这里是int*/
typedef struct
{
	ElemType data[MAXSIZE];	/*数组， 存储数据元素*/
	int length;				/*线性表当前长度*/
}SqList;

// 初始化链表
Status InitList(SqList* L);

//链表是否为空
Status ListEmpty(SqList L);

//将线性表清空
Status ClearList(SqList* L);

//将线性表L中第i个元素返回给e
Status GetElem(SqList L, int i, ElemType* e);

