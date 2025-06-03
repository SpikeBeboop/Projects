/*
*	≤‚ ‘
*/
#define __TEST__
//#define __SQL_LIST__

#ifdef __TEST__
#include <stdio.h>
#include <string.h>

int main(void)
{
	int a[10];
	memset(a, 0, sizeof(a));
	for (int i = 0; i < 10; i++)
	{
		printf("%d\n", a[i]);
	}
	return 0;
}
#endif // __TEST__

/*
*	À≥–Ú±Ì
*/
#ifdef __SQL_LIST__
#include <stdio.h>

int main(void)
{
	return 0;
}
#endif // __SQL_LIST__
