#include <queue> // Include queue for BFS

int orientation;
int board[24][12];
bool visited[24][12];


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

// Struct to hold the coordinates of each cell in the grid
struct Cell {
  int x, y;
};

// BFS-based wavefront function
void waveFront(int goalX, int goalY) {
  // Directions for moving to neighboring cells (north, east, south, west)
  int dx[] = {0, 1, 0, -1};
  int dy[] = {1, 0, -1, 0};

  for(int i = 0; i < 24; i++){
    for(int j = 0; j < 12; j++){
      if (board[i][j] != 150){
        board[i][j] = 999;
      }
    }
  }
  // Create a queue to hold cells for BFS
  std::queue<Cell> q;
  
  // Start the wavefront at the goal cell
  q.push({goalX, goalY});
  board[goalX][goalY] = 0; // Distance to the goal itself is 0
  
  // BFS to propagate the wavefront
  while (!q.empty()) {
    // Get the current cell
    Cell current = q.front();
    q.pop();
    
    // Get the distance of the current cell
    int currentDistance = board[current.x][current.y];
    
    // Visit all 4 neighbors (north, east, south, west)
    for (int i = 0; i < 4; i++) {
      int newX = current.x + dx[i];
      int newY = current.y + dy[i];
      
      // Check if the neighbor is within bounds and not an obstacle
      if (newX >= 0 && newX < 24 && newY >= 0 && newY < 12 && board[newX][newY] != 150) {
        // If the neighbor hasn't been visited (i.e., has a value of 999)
        if (board[newX][newY] == 999) {
          // Set the neighbor's distance as currentDistance + 1
          board[newX][newY] = currentDistance + 1;
          
          // Enqueue the neighbor to process its neighbors in the future
          q.push({newX, newY});
         }
       }
     }
   }
}
void move(int orien, int dxn, int min) {
  // If the robot is facing the correct direction, just move forward
  if (orien == dxn) {
    Serial.print("F, ");  // Move Forward
    Serial.println(min);
  }
  // Turn right
  else if ((orien + 1) % 4 == dxn) {
    Serial.print("R, ");  // Turn Right
    Serial.println(min);
    orientation = dxn;  // Update orientation after turning right
  }
  // Turn left
  else if ((orien + 3) % 4 == dxn) {
    Serial.print("L, ");  // Turn Left
    Serial.println(min);
    orientation = dxn;  // Update orientation after turning left
  }
  // 180-degree turn (reverse)
  else if ((orien + 2) % 4 == dxn) {
    Serial.print("180 F, ");  // Reverse turn
    Serial.println(min);
    orientation = dxn;  // Update orientation after turning 180 degrees
  }
}

int return_orientation(){
  return orientation; 
}

void markVisited(int x, int y){
  visited[x][y] = true;
}

// Function to find the path from startX, startY to the goal using the wavefront
void findPath(int startX, int startY, int goalX, int goalY) {
  // Directions for moving to neighboring cells (north, east, south, west)
  int dx[] = {0, 1, 0, -1};
  int dy[] = {1, 0, -1, 0};

  // Reset the visited array
  for (int i = 0; i < 24; i++) {
    for (int j = 0; j < 12; j++) {
      visited[i][j] = false;
    }
  }

  // Start the pathfinding from the starting point
  int currentX = startX;
  int currentY = startY;

  // Traverse until we reach the goal
  while (currentX != goalX || currentY != goalY) {
    // Mark the current cell as visited
    visited[currentX][currentY] = true;

    // Variables to track the next move
    int minDistance = 999;  // Start with a large value
    int nextX = currentX;
    int nextY = currentY;
    int bestDirection = -1; // To store the best direction to move
    
    // Check all four neighboring cells
    for (int i = 0; i < 4; i++) {
      int newX = currentX + dx[i];
      int newY = currentY + dy[i];

      // Ensure the neighbor is within bounds and not visited or an obstacle
      if (newX >= 0 && newX < 24 && newY >= 0 && newY < 12 && !visited[newX][newY] && board[newX][newY] != 150) {
        // Find the neighbor with the smallest wavefront value
        if (board[newX][newY] < minDistance) {
          minDistance = board[newX][newY];
          nextX = newX;
          nextY = newY;
          bestDirection = i;  // Store the best direction index
        }
      }
    }

    // If no valid move was found, stop (could happen in some edge cases)
    if (minDistance == 999) {
      Serial.println("No valid path found!");
      return;
    }

    // Output the move command (using your `move()` function)
    move(return_orientation(), bestDirection, minDistance);

    // Move to the next cell
    currentX = nextX;
    currentY = nextY;

    // Print current position for debugging
    Serial.print("Moving to: (");
    Serial.print(currentX);
    Serial.print(", ");
    Serial.print(currentY);
    Serial.println(")");
  }

  // When the goal is reached
  Serial.println("Goal reached!");
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //North = 0, east = 1, south = 2, west = 3
  orientation = 0;
  //  createObjects(2,9);
  //  createObjects(5,5);
  delay(2000);
  waveFront(3,2);
  delay(2000);
  displayBoard();
  //startX, startY, goalX, goalY
  findPath(0, 11, 3, 2);
}

void loop() {
  // put your main code here, to run repeatedly:

}