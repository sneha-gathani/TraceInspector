function precompute(diri)
{
    //Line number of ith element pushed onto this every iteration
    var stack = new buckets.Stack();
    //counts height where block needs to end
    var all_elements_height = new buckets.Stack();
    //stores [x_position, y_position]
    var positions_stack = new buckets.Stack();
    //stores which column this stack element belongs to
    var c = new buckets.Stack();

    var i = 0, j = 1;
    var x_position = 10;
    var y_position = 10;
    var in_between_space = 5;
    var width = 40;
    var height = 25;
    var column = 0;

    var precomputed_position = [];
    var rect_data = []

    //this will be used in the next iteration --> Captures all 4 coordinates of all the rectangles in [[[x1,y1][x2,y2][x3,y3][x4,y4]],[[x1,y1][x2,y2][x3,y3][x4,y4]], ... ] format
    var later_use = [];

    //checks if i and j are same
    function check_ij(i, j)
    {
        if(diri[i].Type == "API")
            return true;
        else if(diri[i].Direction == ">" && diri[j].Direction == "<" && diri[i].Method == diri[j].Method && diri[i].Args == diri[j].Args)
            return true;
        else
            return false;
    }

    //for 1st i and j not same
    if(!check_ij(i, j))
    {
        stack.push(i);
        c.push(column);
        positions_stack.push([x_position, y_position]);
        all_elements_height.push(0);

        x_position = x_position + width + in_between_space;
        y_position = y_position + height + in_between_space;

        column = column + 1;
        i = i + 1;
        j = j + 1;
    }

    //until i is last element and j is no element or i is second last element and j is last element
    while(i < diri.length && j < diri.length)
    {
        if(stack.peek() == i)
        {
            console.log("A");
            var val = {"Type": diri[i].Type, "Thread_ID": diri[i].Thread_ID, "Method": diri[i].Method + '(' + diri[i].Args + ')', "Function": diri[i].Function};
            rect_data.push(val);

            var temp = [positions_stack.peek()[0], positions_stack.peek()[1]];
            temp.push(height + (all_elements_height.peek() * (height + in_between_space)));
            precomputed_position.push(temp)

            var coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]];
            var coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]];
            var coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
            var coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
            var temporary = [];
            temporary.push(coordinate_a, coordinate_b, coordinate_c, coordinate_d)

            later_use.push(temporary);

            x_position = x_position - (width + in_between_space);
            column = column - 1;
            i = i + 2;
            j = j + 2;
            stack.pop();
            c.pop();
            positions_stack.pop();
            all_elements_height.pop();
        }
        console.log("looking at")
        console.log(stack.toArray());
        stack.push(i);
        console.log(stack.toArray());
        c.push(column);
        console.log("dhfsjhfksdhfio");
        positions_stack.push([x_position, y_position]);
        console.log(positions_stack.toArray())
        all_elements_height.push(0);

        //checking i with the top of the stack
        //if ith element is same as the top of the element
        var to_check = stack.toArray();

        if(to_check.length == 1)
        {
            console.log("B");
            x_position = x_position + width + in_between_space;
            y_position = y_position + height + in_between_space;

            column = column + 1;

            stack.push(j);
            c.push(column);
            positions_stack.push([x_position, y_position]);
            all_elements_height.push(0);

            var to_check = stack.toArray();
        }

        if(check_ij(to_check[1], to_check[0]))
        {

            console.log("C");
            stack.pop();
            c.pop();
            positions_stack.pop();
            all_elements_height.pop();

            var val = {"Type": diri[i].Type, "Thread_ID": diri[i].Thread_ID, "Method": diri[i].Method + '(' + diri[i].Args + ')', "Function": diri[i].Function};
            rect_data.push(val);

            var temp = [positions_stack.peek()[0], positions_stack.peek()[1]];
            temp.push(height + (all_elements_height.peek() * (height + in_between_space)));
            precomputed_position.push(temp);

            var coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]];
            var coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]];
            var coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
            var coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
            var temporary = [];
            temporary.push(coordinate_a, coordinate_b, coordinate_c, coordinate_d)

            later_use.push(temporary);

            if(c.peek() < column)
            {
                column = column - 1;
                x_position = x_position - (width + in_between_space);
            }

            console.log("Trial");
            console.log(stack.toArray());
            stack.pop();
            console.log(stack.toArray());
            c.pop();
            positions_stack.pop();
            all_elements_height.pop();

            i = i + 1;
            j = j + 1;
        }

        //if ith element is not the same as the top of the stack
        else
        {

            console.log("D");
            //check with jth element
            //if it is the same as the jth element
            if(check_ij(i, j))
            {

                console.log("E");
                var val = {"Type": diri[i].Type, "Thread_ID": diri[i].Thread_ID, "Method": diri[i].Method + '(' + diri[i].Args + ')', "Function": diri[i].Function};
                rect_data.push(val);

                var temp = [x_position, y_position];
                temp.push(height);
                precomputed_position.push(temp);

                var coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]];
                var coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]];
                var coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
                var coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
                var temporary = [];
                temporary.push(coordinate_a, coordinate_b, coordinate_c, coordinate_d)

                later_use.push(temporary);

                stack.pop();
                c.pop();
                positions_stack.pop();
                all_elements_height.pop();

                var a = all_elements_height.toArray();
                all_elements_height.clear();
                var sh;
                for(sh = a.length - 1; sh >= 0; sh--)
                {
                    a[sh] = a[sh] + 1;
                    all_elements_height.push(a[sh]);
                }

                if(c.peek() >= column && c.peek() != 0)
                {
                    column = column - 1;
                    x_position = x_position - (width + in_between_space);                      
                } 

                y_position = y_position + height + (in_between_space);
                i = i + 2;
                j = j + 2;
            }
            //if it is not same as the jth element
            else
            {

            console.log("F");
                var a = all_elements_height.toArray();
                all_elements_height.clear();
                var sh;
                for(sh = a.length - 1; sh >= 1; sh--)
                {
                    a[sh] = a[sh] + 1;
                    all_elements_height.push(a[sh]);
                }
                all_elements_height.push(a[0]);

                y_position = y_position + height + in_between_space; 
                x_position = x_position + width + in_between_space;

                column = column + 1;
                i = i + 1;
                j = j + 1;
            }
        }
    }

    //Point where i is last element and j is out of that diri array
    if((i == (diri.length - 1) && j >= diri.length))
    {

            console.log("G");
        y_position = y_position + (4 * in_between_space);

        stack.push(i);
        c.push(column);
        positions_stack.push([x_position, y_position]);
        all_elements_height.push(0);

        //if ith element is not the same as the top of the element
        if(!check_ij(stack.peek(), i))
        {
            if(stack.toArray().length == 1)
            {

            console.log("H");
                var val = {"Type": diri[i].Type, "Thread_ID": diri[i].Thread_ID, "Method": diri[i].Method + '(' + diri[i].Args + ')', "Function": diri[i].Function};
                rect_data.push(val);

                var temp = [x_position, y_position];
                temp.push(height);
                precomputed_position.push(temp);

                var coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]];
                var coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]];
                var coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
                var coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
                var temporary = [];
                temporary.push(coordinate_a, coordinate_b, coordinate_c, coordinate_d)

                later_use.push(temporary);
            }

            //if ith element is the same as top element in the stack
            else
            {

            console.log("I");
                var val = {"Type": diri[i].Type, "Thread_ID": diri[i].Thread_ID, "Method": diri[i].Method + '(' + diri[i].Args + ')', "Function": diri[i].Function};
                rect_data.push(val);

                stack.pop();
                c.pop();
                positions_stack.pop();
                all_elements_height.pop();

                var temp = [positions_stack.peek()[0], positions_stack.peek()[1]];
                temp.push(height + (all_elements_height.peek() * (height + in_between_space)));
                precomputed_position.push(temp);

                var coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]];
                var coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]];
                var coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
                var coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
                var temporary = [];
                temporary.push(coordinate_a, coordinate_b, coordinate_c, coordinate_d)

                later_use.push(temporary);
                
                stack.pop();
                c.pop();
                positions_stack.pop();
                all_elements_height.pop();
            }
        }   
    }
    while(!stack.isEmpty())
    {

            console.log("J");
        var val = {"Type": diri[stack.peek()].Type, "Thread_ID": diri[stack.peek()].Thread_ID, "Method": diri[stack.peek()].Method + '(' + diri[stack.peek()].Args + ')', "Function": diri[stack.peek()].Function};
        rect_data.push(val);

        var temp = [positions_stack.peek()[0], positions_stack.peek()[1]];
        temp.push(height + (all_elements_height.peek() * (height + in_between_space)));
        precomputed_position.push(temp);

        var coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]];
        var coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]];
        var coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
        var coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))];
        var temporary = [];
        temporary.push(coordinate_a, coordinate_b, coordinate_c, coordinate_d)

        later_use.push(temporary);

        stack.pop();
        c.pop();
        positions_stack.pop();
        all_elements_height.pop();
    }
    console.log("Array of all positions");
    console.log(later_use);
    console.log("Size:");
    console.log(later_use.length);

    return [precomputed_position, rect_data];
}