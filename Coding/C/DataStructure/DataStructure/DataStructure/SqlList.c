#include "SqlList.h"

Status InitList(SqlList* L)
{
	L = malloc(sizeof(SqlList));
	//判断创建空间是否成功
	if (L == NULL)
		return FALSE;
	//数据初始化为0，并将长度设置为0；
	memset(L->data, 0, sizeof(ElemType)*MAXSIZE);
	L->length = 0;
	return TRUE;
}

Status ListEmpty(SqlList L)
{
	if (L.length == 0)
		return TRUE;
	else
		return FALSE;
}

Status ClearList(SqlList* L)
{
	if (L == NULL)
		return FALSE;
	
	L->length = 0;

	return TRUE;
}

Status GetElem(SqlList L, int i, ElemType* e)
{
	if (i < 0 || i >= L.length)
		return FALSE;
	*e = L.data[i];
	return TRUE;
}
