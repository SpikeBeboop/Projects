#include <stdio.h>
#include <conio.h>
#include <Windows.h>

#define HEIGHT 20
#define WIDTH 80

/*
* ����
*/
//��ָ��λ�ô�ӡ�ַ�
void gotoxy(int x, int y)
{
	COORD coord;
	coord.X = x;
	coord.Y = y;
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

/*
* ͼ��������
*/
void draw()
{

}

//��ͼ����
void drawmap()
{
	for (int i = 0; i < HEIGHT; i++)
	{
		gotoxy(0, i);
		putchar('*');
		gotoxy(WIDTH, i);
		putchar('*');
	}

	for (int i = 1; i < WIDTH; i++)
	{
		gotoxy(i, 0);
		putchar('*');
	}
}

/*
* �������к���
*/
void run_game()
{
	drawmap();
	gotoxy(0, HEIGHT + 10);
	while (1)
	{
		
	}
}


int main(void)
{
	run_game();
	return 0;
}