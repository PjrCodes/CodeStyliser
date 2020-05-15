#include <stdio.h>
int main()
{
   
   
    /// FOR, IF, WHILE, DO, SWITCH, if this is the FIRST charecter of nxt Line after a loop/ condition/ blaha bla, Then IGNORE.  
failure 2.
macros.. there are some macros in cfiles also. like conffileapi.c

// failure 3.
//      for (parse_data=data; parse_data->param_name; parse_data++)
//          switch(parse_data->param_type) {
//             defailt: 
//             assadpods;
//          }


failure 4:
-    ifc = 0;
-    iflist->count = 0;
-
+    ifc = 0; {
+    iflist->count = 0; {
+    }



// failure 6:
//              }
// -            if(epd_stack == US_STACK_EPD)
// +            if(epd_stack == US_STACK_EPD) {
//                  len += 2; /* Increase the len to remove the WSMP ethertype */
// -            else
// +            else {
//                  len += sizeof(lpd); /* Increate len to remove LPD header */
//              recv_data->length = ret - len;
// -            recv_data->data = buffer + len;
// +            }
// +             }
// +             recv_data->data = buffer + len;
//              return SV2X_RADIOSTATUS_SUCCESS;
//          }
//      }

// failure 7:
// +    if ( f->diff ) f->cw = (w0 * w0) * (sampling_time_secs); {
// +    else           f->cw = (w0 * w0) * (sampling_time_secs * sampling_time_secs); {
// +    }

// failure 8:
//   * @Description Function to fill the blackbox diagnose information
// -                    for the requested region *
// +                    for the requested region * {

// failure 9:
//  #if (TEST_CODE & ENABLE_DNPW_APP)
// -    if (TRUE && dnpw_d->cur_veh)
// +    if (TRUE && dnpw_d->cur_veh) {
//  #else
//      if ((rv->rv_d.delta_heading <= (D_ZERO + dnpw_cfg->max_delta_heading) ||
//          (rv->rv_d.delta_heading >= (D_360 - dnpw_cfg->max_delta_heading))) &&
// @@ -204,7 +204,8 @@ dnpw_veh_selector(struct rv_list *rv,struct blackbox_ctx *ctx)
//  #endif

// failure 10:
//      if (hvCam->positional_accuracy.semi_minor_axis_accuracy ==
//                                      SemiAxisLength_unavailable) {
//          bsm->positionalaccuracy[1] =  ETSI_SEMI_MIN_CONF_NAV;


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