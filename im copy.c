// LATEST ERRORS FILE

// err 2: MACRO-error:
//    } added after \
// fix: add the } before \ if when you are inserting there is a \
      
//    else  *dst = NULL;  \ 

 
// err 3: SAME-LINE-PARENTHESES-error: 
//    {} added after last ) but must be added after (condition) parenthes

// if ( f->diff ) f->cw = (w0 * w0) * (sampling_time_secs);
// else f->cw = (w0 * w0) * (sampling_time_secs * sampling_time_secs);
// else f->y[f->ny] = current_value;


// err 5: KEYWORD-error:
//    # error, mustnt add {} if next line after curlyBraceIndexLine has a Preprocesser
// fix: logic to be  used is that wherever you are putting { after that line there shouldnt be a # as the first character in the line. 

// if (rv->rv_d.dc < dnpw_cfg->samelane_right_edge_mts)))
//    #endif



// err 7: PARENTH_AFTER_FOR_error:
//    even if parenth are not immedieatly after, it gives error
// fix: check that () are JUST after for. 
//    * this example also shows SAME-LINE-PARENTHESES-error:

//             foreign_vel = IAV_DRIVE_FOREIGN_VEL(rawmsg);

// you need to check that the ( is just after for. 


// err 6: FUNCTION-error:
//    after function ended, we see some lines added, something to do with double line if
//    potential problem: to do with insert statement
// potential fix: when reading lines, copy into another temp list, and then take temp list and put into main file. 
// potential error: random lines input

//    if(asdadsoiapdsoas.0[p['p.-sa.xass']]

// asdasdasd[psda]
//     asdas0>asasd-0ads=.d
//  )
asd; //  asdpo; //as-doi-ad()PI@(>)
// bb_deint_0:
//    if ( asdd && 
//    asdo) {
// ad; /*       bb_Cfg_(asd); */
// //       free(asd);
// //       act->as = NULL;
// /*    }
//     return V2X_EINVAL; */ sadpo;
// asd; // }

// adsop;
// adpo;

//             last __LITTLE_ENDIAN__
// /* adsoi
// */ commentover;