#include <stdio.h>
int main()
{
   
   
    
failure 2:
macros.. there are some macros in cfiles also. like conffileapi.c

failure 3:
   //   for (parse_data=data; parse_data->param_name; parse_data++)
   //       switch(parse_data->param_type) {
   //          defailt: 
   //          assadpods;
   //          dsoid:
   //          dsd;
   //       } // THese are detected as {} for the for
   // fix: /// FOR, IF, WHILE, DO, SWITCH, if this is the FIRST charecter of nxt Line after a loop/ condition/ blaha bla, Then IGNORE.  



failure 7: sameln error
//     if ( f->diff ) f->cw = (w0 * w0) * (sampling_time_secs); 
//     else           f->cw = (w0 * w0) * (sampling_time_secs * sampling_time_secs); 


failure 8: multiline comment error (leave commented)
/* tries to add {} for such things also:
   for //()
*/

failure 9:
//  #if (TEST_CODE & ENABLE_DNPW_APP)
//    if (TRUE && dnpw_d->cur_veh) // adds here
//  #else
//      if  ((rv->rv_d.delta_heading <= (D_ZERO + dnpw_cfg->max_delta_heading) ||
//          (rv->rv_d.delta_heading >= (D_360 - dnpw_cfg->max_delta_heading))) &&

//  #endif
   fix: if next line (after bracket complete) has "#", then cancel life.


// failure 10: //DO NOW
//      if (hvCam->positional_accuracy.semi_minor_axis_accuracy ==
//                                      SemiAxisLength_unavailable)
//                                      {
//          bsm->positionalaccuracy[1] =  ETSI_SEMI_MIN_CONF_NAV;
//       }
      









// warn 1: i think it because of wherever tab has been used.
// @@ -252,18 +262,20 @@ static int savari_gps_info_recv_msg(struct timeval *sent_tstamp,

//          memset(buf, 0, sizeof(buf));
//      }
//           bytes = recvfrom(nw_ctx->sock, buf, sizeof(buf), 0, NULL, NULL);
// -       if (bytes < 0)
// +       if (bytes < 0) {
//              return -1;
// -
// + }
// + 