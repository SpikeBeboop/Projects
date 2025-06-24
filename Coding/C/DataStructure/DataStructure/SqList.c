#include "SqList.h"

Status InitList(SqList* L)
{
    if (L == NULL)
        return ERROR;
    memset(L->data, 0, MAXSIZE);
    L->length = 0;
    return OK;
}

Status ListEmpty(SqList L)
{
    if (L.length == 0)
        return OK;
    return ERROR;
}

Status ClearList(SqList* L)
{
    if (L == NULL)
        return ERROR;
    memset(L->data, 0, MAXSIZE);
    L->length = 0;
    return OK;
}

Status GetElem(SqList L, int i, ElemType* e)
{
    if (i <= 0 || i >= L.length)
        return ERROR;
    *e = L.data[i - 1];
    return OK;
}
