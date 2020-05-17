#include <stdio.h>
int main()
{


    // for() 
    // ;
    // amainz
    printf("I AM HELLO WOELD");
    // asds
    
    // for (int i = 0; i < 10; i++)
    //     printf("I AM I");   
         // as

    for (int j = 0; j < 10; j++) {
        // check
        printf("I AM j"); 

    }
    for (int k = 0; k < 10; k++)     {
        printf("NO CURLIES k:%d", k);

    }



    

        for (int a = 0; a < 10; a++) {
                // indented check
            printf("NO CURLIES %d \n", a);  
        }


        
        
    for (int p = 0; p < 10; p++) {

        printf("NO CURLIES %d", p); 

    }
    for (int p = 0; p < 10; p++) { /* this should work */

        printf("NO CURLIES %d", p); 
    }
    
    
    
    for (int p = 0; p < 10; p++) 


    // check
    { 
        printf("NO CURLIES %d", p); 
    }




    // TINEE ERROR: (comment Iam disappears)
    for (int p = 0; p < 10; p++) { // I am

        printf("NO CURLIES %d", p); 
    }


}


