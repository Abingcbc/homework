//稳定子
int stablity(int type,int x,int y){
    int row,col,left=0,right=0,up=0,down=0;
    int left_up=0,right_down=0,left_down=0,right_up=0;
    int stability=0;
    if (x>0&&x<15&&y>0&&y<15){
        stability=0;
        for (row=x-1;cheseboard[row][y]==type&&row-1>=0;row--);
        if (cheseboard[row][y]==0)
            left=0;
        else if (cheseboard[row][y]==-type)
            left=-1;
        else if (cheseboard[row][y]==type)
            left=1;
        for (row=x+1;cheseboard[row][y]==type&&row+1<16;row++);
        if (cheseboard[row][y]==0)
            right=0;
        else if (cheseboard[row][y]==-type)
            right=-1;
        else if (cheseboard[row][y]==type)
            right=1;
        if (left==-1&&right==-1)
            stability+=5;
        else if (left==1&&right==1)
            stability+=3;
        else if ((left==-1&&right==0)||(left==0&&right==-1))
            stability-=6;
        else if (left==0&&right==0)
            stability--;
        else if ((left==0&&right==1)||(left==1&&right==0))
            stability+=3;
        else
            stability+=2;//横向
        for (col=y-1;cheseboard[x][col]==type&&col-1>=0;col--);
        if (cheseboard[x][col]==0)
            down=0;
        else if (cheseboard[x][col]==-type)
            down=-1;
        else if (cheseboard[x][col]==type)
            down=1;
        for (col=y+1;cheseboard[x][col]==type&&col+1<16;col++);
        if (cheseboard[x][col]==0)
            up=0;
        else if (cheseboard[x][col]==-type)
            up=-1;
        else if (cheseboard[x][col]==type)
            up=1;
        if (down==-1&&up==-1)
            stability+=5;
        else if (down==1&&up==1)
            stability+=3;
        else if ((down==0&&up==-1)||(down==-1&&up==0))
            stability-=6;
        else if (down==0&&up==0)
            stability--;
        else if ((down==1&&up==0)||(up==1&&down==0))
            stability+=3;
        else
            stability+=2;//竖向
        for (row=x-1,col=y-1;cheseboard[row][col]==type&&row-1>=0&&col-1>=0;row--,col--);
        if (cheseboard[row][col]==0)
            left_up=0;
        else if (cheseboard[row][col]==-type)
            left_up=-1;
        else if (cheseboard[row][col]==type)
            left_up=1;
        for (row=x+1,col=y+1;cheseboard[row][col]==type&&row+1<16&&col+1<16;row++,col++);
        if (cheseboard[row][col]==0)
            right_down=0;
        else if (cheseboard[row][col]==-type)
            right_down=-1;
        else if (cheseboard[row][col]==type)
            right_down=1;
        if (left_up==-1&&right_down==-1)
            stability+=5;
        else if (left_up==1&&right_down==1)
            stability+=3;
        else if ((left_up==0&&right_down==-1)||(left_up==-1&&right_down==0))
            stability-=6;
        else if (left_up==0&&right_down==0)
            stability--;
        else if ((left_up==1&&right_down==0)||(left_up==0&&right_up==1))
            stability+=3;
        else
            stability+=2;//左斜
        for (row=x-1,col=y+1;cheseboard[row][col]==type&&row-1>=0&&col-1<16;row--,col++);
        if (cheseboard[row][col]==0)
            left_down=0;
        else if (cheseboard[row][col]==-type)
            left_down=-1;
        else if (cheseboard[row][col]==type)
            left_down=1;
        for (row=x+1,col=y-1;cheseboard[row][col]==type&&row+1<16&&col-1>=0;row++,col--);
        if (cheseboard[row][col]==0)
            right_up=0;
        else if (cheseboard[row][col]==-type)
            right_up=-1;
        else if (cheseboard[row][col]==type)
            right_up=1;
        if (left_down==-1&&right_up==-1)
            stability+=5;
        else if (left_down==1&&right_up==1)
            stability+=3;
        else if ((left_down==-1&&right_up==0)||(left_down==0||right_up==-1))
            stability-=6;
        else if (left_down==0&&right_up==0)
            stability--;
        else if ((left_down==1&&right_up==0)||(left_down==0&&right_up==1))
            stability+=3;
        else
            stability+=2;//右斜
    }
    else if ((x==0||x==15)&&y>0&&y<15){
        down=0;
        up=0;
        for (col=y-1;cheseboard[x][col]==type&&col-1>=0;col--);
        if (cheseboard[x][col]==0)
            down=0;
        else if (cheseboard[x][col]==-type)
            down=-1;
        else if (cheseboard[x][col]==type)
            down=1;
        for (col=y+1;cheseboard[x][col]==type&&col+1<16;col++);
        if (cheseboard[x][col]==0)
            up=0;
        else if (cheseboard[x][col]==-type)
            up=-1;
        else if (cheseboard[x][col]==type)
            up=1;
        if (down==-1&&up==-1)
            stability+=10;
        else if (down==1&&up==1)
            stability+=40;
        else if ((down==-1&&up==0)||(down==0&&up==-1))
            stability-=30;
        else if (down==0&&up==0)
            stability-=5;
        else if ((down==0&&up==1)||(down==1&&up==0))
            stability+=40;
        else
            stability+=2;//竖向
    }
    else if ((y==0||y==15)&&x>0&&x<15){
        left=0;
        right=0;
        for (row=x-1;cheseboard[row][y]==type&&row-1>=0;row--);
        if (cheseboard[row][y]==0)
            left=0;
        else if (cheseboard[row][y]==-type)
            left=-1;
        else if (cheseboard[row][y]==type)
            left=1;
        for (row=x+1;cheseboard[row][y]==type&&row+1<16;row++);
        if (cheseboard[row][y]==0)
            right=0;
        else if (cheseboard[row][y]==-type)
            right=-1;
        else if (cheseboard[row][y]==type)
            right=1;
        if (left==-1&&right==-1)
            stability+=10;
        else if (left==1&&right==1)
            stability+=40;
        else if ((left==-1&&right==0)||(left==0&&right==-1))
            stability-=30;
        else if (left==0&&right==0)
            stability-=5;
        else if ((left==0&&right==1)||(left==1&&right==0))
            stability+=40;
        else
            stability+=2;//横向
    }
    else if ((x==0&&y==0)||(x==0&&y==15)||(x==15&&y==0)||(x==15&&y==15)){
        stability+=200;
    }
    return stability;
}
