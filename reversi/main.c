//-1代表黑棋。1代表白棋
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <math.h>
int side;
int cheseboard[16][16];//棋盘
int cannotmove[16][16];//是否可以落子
int moveforce[16][16];//棋盘各点行动力
int hidedmoveforce[16][16];//棋盘各点潜在行动力
int totalmove=0;//当前局面共有几个合法落子点
int totalhidedmove=0;//当前局面共有几个潜在落子点
int history[16][16]=
{{7000,-80,10,10,8,8,8,8,8,8,8,8,10,10,-80,7000},
    {-80,-280,2,2,1,1,1,1,1,1,1,1,2,2,-280,-80},
    {10,2,3,1,1,1,1,1,1,1,1,1,1,3,2,10},
    {10,2,1,1,1,1,1,1,1,1,1,1,1,1,2,10},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {10,2,1,1,1,1,1,1,1,1,1,1,1,1,2,10},
    {10,2,3,1,1,1,1,1,1,1,1,1,1,3,2,10},
    {-80,-280,2,2,1,1,1,1,1,1,1,1,2,2,-280,-80},
    {7000,-80,10,10,8,8,8,8,8,8,8,8,10,10,-80,7000},
};//历史表
int location_value_early[16][16]=
{{2000,-300,3,2,2,2,2,2,2,2,2,2,2,3,-300,2000},
    {-300,-800,0,0,0,0,0,0,0,0,0,0,0,0,-800,-300},
    {3,0,3,0,0,0,0,0,0,0,0,0,0,3,0,3},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2},
    {3,0,3,0,0,0,0,0,0,0,0,0,0,3,0,3},
    {-300,-800,0,0,0,0,0,0,0,0,0,0,0,0,-800,-300},
    {2000,-300,3,2,2,2,2,2,2,2,2,2,2,3,-300,2000},
};//棋盘位置估值开局
int location_value_middle[16][16]=
{{7000,-200,10,10,8,8,8,8,8,8,8,8,10,10,-200,7000},
    {-200,-800,2,2,1,1,1,1,1,1,1,1,2,2,-800,-200},
    {10,2,3,1,1,1,1,1,1,1,1,1,1,3,2,10},
    {10,2,1,1,1,1,1,1,1,1,1,1,1,1,2,10},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8},
    {10,2,1,1,1,1,1,1,1,1,1,1,1,1,2,10},
    {10,2,3,1,1,1,1,1,1,1,1,1,1,3,2,10},
    {-200,-800,2,2,1,1,1,1,1,1,1,1,2,2,-800,-200},
    {7000,-200,10,10,8,8,8,8,8,8,8,8,10,10,-200,7000},
};//棋盘位置估值中局
int location_value_final[16][16]=
{{7000,-80,10,10,8,8,8,8,8,8,8,8,10,10,-80,7000},
    {-80,-280,2,2,2,2,2,2,2,2,2,2,2,2,-280,-80},
    {10,2,3,2,2,2,2,2,2,2,2,2,2,3,2,10},
    {10,2,2,2,2,2,2,2,2,2,2,2,2,2,2,10},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,8},
    {10,2,2,2,2,2,2,2,2,2,2,2,2,2,2,10},
    {10,2,3,2,2,2,2,2,2,2,2,2,2,3,2,10},
    {-80,-280,2,2,2,2,2,2,2,2,2,2,2,2,-280,-80},
    {7000,-80,10,10,8,8,8,8,8,8,8,8,10,10,-80,7000},
};//棋盘位置估值终局
struct paixu{
    int x;
    int y;
};//排序
int enermyrow,enermycol;//对面落子
int finalrow = 0,finalcol = 0;//最终落子
clock_t start,finish;
int enermymove,enermyhidedmove;//对面行动力以及潜在行动力
void islegal_by_blank(int type);//通过空格判断可落子点
void islegal_by_blank_for_enermy(int type);//为对面判断行动力
void turnover(int type,int row,int col);//反转棋子
int alphabeta(int depth,int alpha,int beta,int type,const int num,int level);//alphabeta剪枝
int evaluate(int type,const int num);//对当前局面估值
void correct(void);//为c位和星位正名
void quicksort(struct paixu min[],int low,int high);//快速排序
int stable_for_board(int type,int x,int y);
int main(void) {
    cheseboard[7][7]=1;
    cheseboard[8][8]=1;
    cheseboard[7][8]=-1;
    cheseboard[8][7]=-1;
    char waste[6];
    int waste2;
    scanf("%s %d",waste,&waste2);
    printf("OK\n");
    fflush(stdout);
    if (waste2==1)
        side=-1;
    else if (waste2==2)
        side=1;//黑棋为-1，白棋为1
    int num=0;//计数器
    while (num<=253&&scanf("%s",waste)==1){
        if (waste[0]=='P'){
            scanf("%d %d",&enermyrow,&enermycol);
            turnover(-side, enermyrow, enermycol);
        }
        else if (waste[0]=='T'){
            start=clock();
            if (num<=50)
                alphabeta(6, -900000, 200000, side, num, 6);
            else if (num>50&&num<=180)
                alphabeta(4, -900000, 200000, side, num, 4);
            else if (num>180&&num<=240)
                alphabeta(6, -900000, 200000, side, num, 6);
            else if (num>240)
                alphabeta(12, -900000, 20000, side, num, 12);
            turnover(side, finalrow, finalcol);
            printf("%d %d\n",finalrow,finalcol);
            fflush(stdout);
            correct();
        }
        num++;
    }
    return 0;
}
//通过空格判断可落子点并计算当前局面共有几个可落子点和潜在落子点
void islegal_by_blank(int type){
    memset(cannotmove, 0, sizeof(cannotmove));
    int m = 0,n = 0;
    totalmove=0;
    totalhidedmove=0;
    for (int i=0;i<16;i++)
        for (int j=0;j<16;j++)
            if (cheseboard[i][j]==0){
                if (cheseboard[i-1][j]==-type&&i-1>=0){
                    totalhidedmove++;
                    if (i-1==0);
                    else {
                        for (m=i-1;m-1>=0&&cheseboard[m][j]==-type;m--);
                        if (cheseboard[m][j]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断上方
                if (cheseboard[i+1][j]==-type&&i+1<16){
                    totalhidedmove++;
                    if (i+1==15);
                    else {
                        for (m=i+1;m+1<16&&cheseboard[m][j]==-type;m++);
                        if (cheseboard[m][j]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断下方
                if (cheseboard[i][j-1]==-type&&j-1>=0){
                    totalhidedmove++;
                    if (j-1==0);
                    else {
                        for (n=j-1;n-1>=0&&cheseboard[i][n]==-type;n--);
                        if (cheseboard[i][n]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断左侧
                if (cheseboard[i][j+1]==-type&&j+1<16){
                    totalhidedmove++;
                    if (j+1==15);
                    else {
                        for (n=j+1;n+1<16&&cheseboard[i][n]==-type;n++);
                        if (cheseboard[i][n]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断右侧
                if (cheseboard[i-1][j-1]==-type&&i-1>=0&&j-1>=0){
                    totalhidedmove++;
                    if (i-1==0||j-1==0);
                    else {
                        for (m=i-1,n=j-1;m-1>=0&&n-1>=0&&cheseboard[m][n]==-type;m--,n--);
                        if (cheseboard[m][n]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断左上
                if (cheseboard[i-1][j+1]==-type&&i-1>=0&&j+1<16){
                    totalhidedmove++;
                    if (i-1==0||j+1==15);
                    else {
                        for (m=i-1,n=j+1;m-1>=0&&n+1<16&&cheseboard[m][n]==-type;m--,n++);
                        if (cheseboard[m][n]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断左下
                if (cheseboard[i+1][j+1]==-type&&i+1<16&&j+1<16){
                    totalhidedmove++;
                    if (i+1==15||j+1==15);
                    else {
                        for (m=i+1,n=j+1;m+1<16&&n+1<16&&cheseboard[m][n]==-type;m++,n++);
                        if (cheseboard[m][n]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断右下
                if (cheseboard[i+1][j-1]==-type&&i+1<16&&j-1>=0){
                    totalhidedmove++;
                    if (i+1==15||j-1==0);
                    else {
                        for (m=i+1,n=j-1;m+1<16&&n-1>=0&&cheseboard[m][n]==-type;m++,n--);
                        if (cheseboard[m][n]==type){
                            cannotmove[i][j]=1;
                            totalmove++;
                            continue;
                        }
                    }
                }//判断右上
            }
}
//为对面判断行动力
void islegal_by_blank_for_enermy(int type){
    int m = 0,n = 0;
    enermymove=0;
    enermyhidedmove=0;
    for (int i=0;i<16;i++)
        for (int j=0;j<16;j++)
            if (cheseboard[i][j]==0){
                if (cheseboard[i-1][j]==-type&&i-1>=0){
                    enermyhidedmove++;
                    if (i-1==0);
                    else {
                        for (m=i-1;m-1>=0&&cheseboard[m][j]==-type;m--);
                        if (cheseboard[m][j]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断上方
                if (cheseboard[i+1][j]==-type&&i+1<16){
                    enermyhidedmove++;
                    if (i+1==15);
                    else {
                        for (m=i+1;m+1<16&&cheseboard[m][j]==-type;m++);
                        if (cheseboard[m][j]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断下方
                if (cheseboard[i][j-1]==-type&&j-1>=0){
                    enermyhidedmove++;
                    if (j-1==0);
                    else {
                        for (n=j-1;n-1>=0&&cheseboard[i][n]==-type;n--);
                        if (cheseboard[i][n]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断左侧
                if (cheseboard[i][j+1]==-type&&j+1<16){
                    enermyhidedmove++;
                    if (j+1==15);
                    else {
                        for (n=j+1;n+1<16&&cheseboard[i][n]==-type;n++);
                        if (cheseboard[i][n]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断右侧
                if (cheseboard[i-1][j-1]==-type&&i-1>=0&&j-1>=0){
                    enermyhidedmove++;
                    if (i-1==0||j-1==0);
                    else {
                        for (m=i-1,n=j-1;m-1>=0&&n-1>=0&&cheseboard[m][n]==-type;m--,n--);
                        if (cheseboard[m][n]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断左上
                if (cheseboard[i-1][j+1]==-type&&i-1>=0&&j+1<16){
                    enermyhidedmove++;
                    if (i-1==0||j+1==15);
                    else {
                        for (m=i-1,n=j+1;m-1>=0&&n+1<16&&cheseboard[m][n]==-type;m--,n++);
                        if (cheseboard[m][n]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断左下
                if (cheseboard[i+1][j+1]==-type&&i+1<16&&j+1<16){
                    enermyhidedmove++;
                    if (i+1==15||j+1==15);
                    else {
                        for (m=i+1,n=j+1;m+1<16&&n+1<16&&cheseboard[m][n]==-type;m++,n++);
                        if (cheseboard[m][n]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断右下
                if (cheseboard[i+1][j-1]==-type&&i+1<16&&j-1>=0){
                    enermyhidedmove++;
                    if (i+1==15||j-1==0);
                    else {
                        for (m=i+1,n=j-1;m+1<16&&n-1>=0&&cheseboard[m][n]==-type;m++,n--);
                        if (cheseboard[m][n]==type){
                            enermymove++;
                            continue;
                        }
                    }
                }//判断右上
            }
}
//反转棋子
void turnover(int type,int row,int col){
    int x,y;
    for (x=row-1;x-1>=0&&cheseboard[x][col]==-type;x--);
    if (cheseboard[x][col]==type)
        for (;x<=row;x++)
            cheseboard[x][col]=type;//反转上方
    for (x=row+1;x+1<16&&cheseboard[x][col]==-type;x++);
    if (cheseboard[x][col]==type)
        for (;x>=row;x--)
            cheseboard[x][col]=type;//反转下方
    for (y=col-1;y-1>=0&&cheseboard[row][y]==-type;y--);
    if (cheseboard[row][y]==type)
        for (;y<=col;y++)
            cheseboard[row][y]=type;//反转左侧
    for (y=col+1;y+1<16&&cheseboard[row][y]==-type;y++);
    if (cheseboard[row][y]==type)
        for (;y>=col;y--)
            cheseboard[row][y]=type;//反转右侧
    for (x=row-1,y=col-1;x-1>=0&&y-1>=0&&cheseboard[x][y]==-type;x--,y--);
    if (cheseboard[x][y]==type)
        for (;x<=row;x++,y++)
            cheseboard[x][y]=type;//反转左上
    for (x=row+1,y=col-1;x+1<16&&y-1>=0&&cheseboard[x][y]==-type;x++,y--);
    if (cheseboard[x][y]==type)
        for (;x>=row;x--,y++)
            cheseboard[x][y]=type;//反转右上
    for (x=row-1,y=col+1;x-1>=0&&y+1<16&&cheseboard[x][y]==-type;x--,y++);
    if (cheseboard[x][y]==type)
        for (;x<=row;x++,y--)
            cheseboard[x][y]=type;//反转左下
    for (x=row+1,y=col+1;x+1<16&&y+1<16&&cheseboard[x][y]==-type;x++,y++);
    if (cheseboard[x][y]==type)
        for (;x>=row;x--,y--)
            cheseboard[x][y]=type;//反转右下
}
//为c位和星位正名
void correct(void){
    if (cheseboard[0][0]==side){
        location_value_early[0][1]=50;
        location_value_early[1][1]=30;
        location_value_early[1][0]=50;
        location_value_middle[0][1]=50;
        location_value_middle[1][1]=30;
        location_value_middle[1][0]=50;
        location_value_final[0][1]=50;
        location_value_final[1][1]=30;
        location_value_final[1][0]=50;
    }
    if (cheseboard[0][15]==side){
        location_value_early[0][14]=50;
        location_value_early[1][15]=50;
        location_value_early[1][14]=30;
        location_value_middle[0][14]=50;
        location_value_middle[1][15]=50;
        location_value_middle[1][14]=30;
        location_value_final[0][14]=50;
        location_value_final[1][15]=50;
        location_value_final[1][14]=30;
    }
    if (cheseboard[15][0]==side){
        location_value_early[15][1]=50;
        location_value_early[14][1]=30;
        location_value_early[14][0]=50;
        location_value_middle[15][1]=50;
        location_value_middle[14][1]=30;
        location_value_middle[14][0]=50;
        location_value_final[15][1]=50;
        location_value_final[14][1]=30;
        location_value_final[14][0]=50;
    }
    if (cheseboard[15][15]==side){
        location_value_early[15][14]=50;
        location_value_early[15][14]=50;
        location_value_early[14][14]=30;
        location_value_middle[15][14]=50;
        location_value_middle[14][15]=50;
        location_value_middle[14][14]=30;
        location_value_final[15][14]=50;
        location_value_final[14][15]=50;
        location_value_final[14][14]=30;
    }
}
//对当前局面估值
int evaluate(int type,const int num){
    int value=0;
    int x,y;
    if (num<=40){
        islegal_by_blank(type);
        islegal_by_blank_for_enermy(-type);
        for (x=0;x<16;x++)
            for (y=0;y<16;y++){
                if (cheseboard[x][y]!=0){
                    value=value+(location_value_early[x][y])*cheseboard[x][y]/type;
                }
            }
        value=value+(totalmove-enermymove)*12;
    }
    else if (num>40&&num<=200){
        islegal_by_blank(type);
        islegal_by_blank_for_enermy(-type);
        for (x=0;x<16;x++)
            for (y=0;y<16;y++){
                if (cheseboard[x][y]!=0){
                    value=value+(location_value_middle[x][y])*cheseboard[x][y]/type;
                }
            }
        value=value+(totalmove-enermymove)*12+(totalhidedmove-enermyhidedmove)*2;
    }
    else if (num>200&&num<=253){
        islegal_by_blank(type);
        islegal_by_blank_for_enermy(-type);
        for (x=0;x<16;x++)
            for (y=0;y<16;y++){
                if (cheseboard[x][y]!=0){
                    value=value+(location_value_final[x][y])*cheseboard[x][y]/type;
                }
            }
        value=value+(totalmove-enermymove)*12+(totalhidedmove-enermyhidedmove);
    }
    return value;
}
//快速排序
void quicksort(struct paixu min[],int low,int high){
    int i,j,temp,m,n,tempm,tempn;
    if (low>high)
        return;
    temp=history[min[low].x][min[low].y];
    tempm=min[low].x;
    tempn=min[low].y;
    i=low;
    j=high;
    while (i!=j) {
        while (history[min[j].x][min[j].y]>=temp&&i<j)
            j--;
        while (history[min[i].x][min[i].y]<=temp&&i<j)
            i++;
        if (i<j){
            m=min[i].x;
            n=min[i].y;
            min[i].x=min[j].x;
            min[i].y=min[j].y;
            min[j].x=m;
            min[j].y=n;
        }
    }
    min[low].x=min[i].x;
    min[low].y=min[i].y;
    min[i].x=tempm;
    min[i].y=tempn;
    quicksort(min, low, i-1);
    quicksort(min, i+1, high);
}
int alphabeta(int depth,int alpha,int beta,int type,const int num,int level){
    int x,y,score=0,count=0,count2=0;
    struct paixu min_to_max[80];
    int save_of_board[16][16],save_of_move[16][16];
    memset(min_to_max, 0, sizeof(min_to_max));
    finish=clock();
    if (depth<=0||finish-start>=4900||num==252){
        if(num!=252)
            return type/side*evaluate(side, num);
        if (num==252){
            int my_chese_number=0;
            for (int m=0;m<16;m++)
                for (int n=0;n<16;n++)
                    if (cheseboard[m][n]==side)
                        my_chese_number++;
            return type/side*my_chese_number;
        }
    }
    islegal_by_blank(type);
    memset(save_of_move, 0, sizeof(save_of_move));
    memcpy(save_of_move, cannotmove, sizeof(cannotmove));
    for (x=0;x<16;x++)
        for (y=0;y<16;y++)
            if (save_of_move[x][y]==1){
                min_to_max[count2].x=x;
                min_to_max[count2].y=y;
                count2++;
            }
    count2--;
    quicksort(min_to_max, 0, count2);
    if (count2<0){//跳步
        islegal_by_blank_for_enermy(-type);
        if (enermymove==0){
            int my_chese_number=0;
            for (int m=0;m<16;m++)
                for (int n=0;n<16;n++)
                    if (cheseboard[m][n]==side)
                        my_chese_number++;
            if (my_chese_number==0)
                my_chese_number=500;
            else my_chese_number=-500;
            return -type/side*my_chese_number;
        }
        return -alphabeta(depth, -beta, -alpha, -type, num, level);
    }
    else {
        for (;count2>=0;count2--){
            score=0;
            x=min_to_max[count2].x;
            y=min_to_max[count2].y;
            memcpy(save_of_board, cheseboard, sizeof(cheseboard));
            turnover(type, x, y);
            score=-alphabeta(depth-1, -beta, -alpha, -type, num+1,level);
            memcpy(cheseboard, save_of_board, sizeof(save_of_board));
            if (count<=0&&depth==level){
                count++;
                finalrow=x;
                finalcol=y;
            }
            if (score>alpha){
                alpha=score;
                history[x][y]=history[x][y]+pow(2, depth);
                if (depth==level){
                    finalrow=x;
                    finalcol=y;
                }
            }
            if (alpha>=beta){
                history[x][y]=history[x][y]+pow(4, depth);
                return alpha;
            }
        }
    }
    return alpha;
}
