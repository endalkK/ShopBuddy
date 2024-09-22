int board[24][12];
int startX;
int startY;
int orientation;
int already = 0;
//North = 0, east = 1, south = 2, west = 3
void displayBoard(){
  int x = 0;
  int y = 0;
  for (y=11;y>-1;y--){
    for (x=0; x<23; x++){
      Serial.print(board[x][y]);
      Serial.print("\t");
    }
    Serial.println(board[x][y]);
    
  }
}

//This creates objects and give them padding of 150
void createObjects(int a, int b){
  //padding
    for(int i = a-1; i < a+2; i++){
      for(int j = b-1; j < b+2; j++){
       if((0 <= i) && (i<24) && (0 <= j) && (j <12)){
          board[i][j] = 150;
        }        
      }
   }
}
//This function will implement wavefront planner motion planing. how far away you are from the goal determine your 
void waveFront(int goalX, int goalY){
  for(int i = 0; i < 24; i++){
      for(int j = 0; j < 12; j++){
        board[i][j] = abs(goalX-i) + abs(goalY - j);
      }
   }
}
int return_orientation(){
  return orientation; 
}
void location(int i){
  if (i == 0)
    startY = startY + 1;
  else if (i == 1)
    startY = startY - 1;
  else if (i == 2)
    startX = startX + 1;
  else if (i == 3)
    startX = startX - 1;
}

void move(int orien, int dxn, int min){
  if (orien == dxn){
      Serial.print("F, ");
      Serial.println(min);
      MoveForward(10);
      Stop();
    }
  else{
    if((orien ==0 && dxn ==2) || (orien ==1 && dxn ==2) || (orien ==2 && dxn ==1) || (orien ==3 && dxn ==0)){
      orientation = dxn;
      Serial.print("R, ");
      Serial.println(min);
      TurnRight();
    }
    else if((orien ==0 && dxn ==3) || (orien ==1 && dxn ==3) || (orien ==2 && dxn ==0) || (orien ==3 && dxn ==1)){
      orientation = dxn;
      Serial.print("L, ");
      Serial.println(min);
      TurnLeft();
    }
    else if((orien ==0 && dxn ==1) || (orien ==1 && dxn ==0) || (orien ==2 && dxn ==3) || (orien ==3 && dxn ==2)){
      already = 1;
      orientation = dxn;
      Serial.print("180 F, ");
      Serial.println(min);
      MoveForward(10);
      Stop();
    }
  }
}

void findPath(){ 
 
  while(board[startX][startY] != 0){
  int min = 150; // float('inf') in python, since our obstacle is the maximum we will have on the board
  int index = 0;
  int negh[] = {150, 150, 150, 150}; //board[startX][startY+1], board[startX][startY-1], board[startX+1][startY], board[startX-1][startY]

  if (startY+1 < 12)
      negh[0] = board[startX][startY+1];
  if (startY-1 > 0)
      negh[1] = board[startX][startY-1];
  if (startX+1 < 24)
      negh[2] = board[startX+1][startY];
  if (startX-1 > 0)
      negh[3] = board[startX-1][startY];
  //
  if (already == 1)
    board[startX][startY] = 150;

  for(int i = 0; i < 4; i++){
    if (negh[i]< min){
      min = negh[i];
      index = i;
    }
  }
  move(return_orientation(), index, min);
  location(index);
  }
}
