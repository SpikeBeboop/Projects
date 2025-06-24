#include <graphics.h>

#include <stdio.h>

int main()
{
	//printf("%ws", GetEasyXVer());

	initgraph(1280, 720);

	int x = 300;
	int y = 300;

	BeginBatchDraw();

	while (true)
	{
		ExMessage msg;
		while (peekmessage(&msg))
		{
			x = msg.x;
			y = msg.y;
		}
		cleardevice();
		solidcircle(x, y, 100);
		FlushBatchDraw();
	}
	EndBatchDraw();

	return 0;
}