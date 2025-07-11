#include <graphics.h>

char board_data[3][3] =
{
	{'-','-','-'},
	{'-','-','-'},
	{'-','-','-'},
};

char current_piece = 'O';

//检测指定棋子的玩家是否获胜
bool CheckWin(char c)
{
	if (board_data[0][0] == c && board_data[0][1] == c && board_data[0][2] == c)
		return true;
	if (board_data[1][0] == c && board_data[1][1] == c && board_data[1][2] == c)
		return true;
	if (board_data[2][0] == c && board_data[2][1] == c && board_data[2][2] == c)
		return true;
	if (board_data[0][0] == c && board_data[1][0] == c && board_data[2][0] == c)
		return true;
	if (board_data[0][1] == c && board_data[1][1] == c && board_data[2][1] == c)
		return true;
	if (board_data[0][2] == c && board_data[1][2] == c && board_data[2][2] == c)
		return true;
	if (board_data[0][0] == c && board_data[1][1] == c && board_data[2][2] == c)
		return true;
	if (board_data[0][2] == c && board_data[1][1] == c && board_data[2][0] == c)
		return true;
	return false;
}

//检测是否出现平局
bool CheckDraw()
{
	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++)
			if (board_data[i][j] == '-')
				return false;
	return true;
}

//绘制棋盘网格
void DrawBord()
{
	line(0, 200, 600, 200);
	line(0, 400, 600, 400);
	line(200, 0, 200, 600);
	line(400, 0, 400, 600);
}

// 绘制棋子
void DrawPiece()
{
	for (size_t i = 0; i < 3; i++)
	{
		for (size_t j = 0; j < 3; j++)
		{
			switch (board_data[i][j])
			{
			case 'O':
				circle(j * 200 + 100, i * 200 + 100, 100);
				break;
			case 'X':
				line(j * 200, i * 200, j * 200 + 200, i * 200 + 200);
				line(j * 200 + 200, i * 200, j * 200, i * 200 + 200);
				break;
			default:
				break;
			}
		}
	}
}

//绘制提示信息
void DrawTipText()
{
	static TCHAR str[64];
	_stprintf_s(str, _T("当前棋子类型: %c"), current_piece);

	settextcolor(RGB(255, 175, 45));
	outtextxy(0, 0, str);
}

int main()
{
	initgraph(600, 600);

	bool running = true;

	ExMessage msg;

	BeginBatchDraw();

	while (running)
	{

		DWORD start_time = GetTickCount();

		while (peekmessage(&msg))
		{

			//检测鼠标左键按下的消息
			if (msg.message == WM_LBUTTONDOWN)
			{

				//计算点击位置

				int x = msg.x;
				int y = msg.y;

				int index_x = x / 200;
				int index_y = y / 200;

				//尝试落子

				if (board_data[index_y][index_x] == '-')
				{
					board_data[index_y][index_x] = current_piece;

					//切换棋子类型

					if (current_piece == 'X')
						current_piece = 'O';
					else
						current_piece = 'X';
				}
			}

		}

		cleardevice();

		DrawBord();
		DrawPiece();
		DrawTipText();

		FlushBatchDraw();

		if (CheckWin('X'))
		{
			MessageBox(GetHWnd(), _T("X 玩家获胜"), _T("游戏结束"), MB_OK);
			running = false;
		}
		else if (CheckWin('O'))
		{
			MessageBox(GetHWnd(), _T("O 玩家获胜"), _T("游戏结束"), MB_OK);
			running = false;
		}
		else if (CheckDraw())
		{
			MessageBox(GetHWnd(), _T("平局！"), _T("游戏结束"), MB_OK);
			running = false;
		}

		DWORD end_time = GetTickCount();
		DWORD delta_time = end_time - start_time;

		if (delta_time < 1000 / 60)
		{
			Sleep(1000 / 60 - delta_time);
		}
	}

	EndBatchDraw();

	return 0;
}