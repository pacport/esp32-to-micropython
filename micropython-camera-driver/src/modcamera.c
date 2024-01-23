/*
 * Copyright [2021] Mauro Riva <info@lemariva.com>
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <string.h>
#include "py/nlr.h"
#include "py/obj.h"
#include "modcamera.h"
#include "py/runtime.h"
#include "py/binary.h"

#if MODULE_CAMERA_ENABLED

#include "esp_system.h"
#include "spi_flash_mmap.h"
#include "esp_camera.h"
#include "esp_log.h"



typedef struct _camera_obj_t {
    int8_t                 id;
    camera_config_t        config;
    bool                   used;
} camera_obj_t;

//STATIC camera_obj_t camera_obj;
STATIC bool camera_init_helper(camera_obj_t *camera, size_t n_pos_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    camera_config_t camera_config = {
    .pin_pwdn = CAM_PIN_PWDN,
    .pin_reset = CAM_PIN_RESET,
    .pin_xclk = CAM_PIN_XCLK,
    .pin_sscb_scl = CAM_PIN_SIOC,
    .pin_sccb_sda = CAM_PIN_SIOD,
    .sccb_i2c_port = 0,

    .pin_d7 = CAM_PIN_D7,
    .pin_d6 = CAM_PIN_D6,
    .pin_d5 = CAM_PIN_D5,
    .pin_d4 = CAM_PIN_D4,
    .pin_d3 = CAM_PIN_D3,
    .pin_d2 = CAM_PIN_D2,
    .pin_d1 = CAM_PIN_D1,
    .pin_d0 = CAM_PIN_D0,
    .pin_vsync = CAM_PIN_VSYNC,
    .pin_href = CAM_PIN_HREF,
    .pin_pclk = CAM_PIN_PCLK,

    //XCLK 20MHz or 10MHz for OV2640 double FPS (Experimental)
    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,
    .pixel_format = PIXFORMAT_RGB565, //YUV422,GRAYSCALE,RGB565,JPEG
    .frame_size = FRAMESIZE_SVGA,    //QQVGA-UXGA Do not use sizes above QVGA when not JPEG

    .jpeg_quality = 12,            //0-63 lower number means higher quality
    .fb_count = 2,                 //if more than one, i2s runs in continuous mode. Use only with JPEG
    .grab_mode = CAMERA_GRAB_WHEN_EMPTY,
};
    
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Camera Init Failed");
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("Camera Init Failed"));
        return false;
    }

    return true;
}


STATIC mp_obj_t camera_init(mp_uint_t n_pos_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    
    camera_obj_t camera_obj;

    bool camera = camera_init_helper(&camera_obj, n_pos_args - 1, pos_args + 1, kw_args);
    if (camera) {
        return mp_const_true;
    }
    else
    {
        return mp_const_false;
    }
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(camera_init_obj, 1, camera_init);


STATIC mp_obj_t camera_deinit(){
    esp_err_t err = esp_camera_deinit();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Camera deinit Failed");
        return mp_const_false;
    }

    return mp_const_true;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(camera_deinit_obj, camera_deinit);


STATIC mp_obj_t camera_capture(){
    //acquire a frame
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
        ESP_LOGE(TAG, "Camera Capture Failed");
        return mp_const_false;
    }

    mp_obj_t image = mp_obj_new_bytes(fb->buf, fb->len);

    //return the frame buffer back to the driver for reuse
    esp_camera_fb_return(fb);
    return image;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(camera_capture_obj, camera_capture);

STATIC mp_obj_t camera_flip(mp_obj_t direction){
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Flipping Failed");
        return mp_const_false;
      }
    int dir = mp_obj_get_int(direction);
    s->set_vflip(s, dir);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_flip_obj, camera_flip);

STATIC mp_obj_t camera_mirror(mp_obj_t direction){
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Mirroring Failed");
        return mp_const_false;
      }
    int dir = mp_obj_get_int(direction);
    s->set_hmirror(s, dir);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_mirror_obj, camera_mirror);

STATIC mp_obj_t camera_framesize(mp_obj_t what){
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Framesize Failed");
        return mp_const_false;
      }
    int size = mp_obj_get_int(what);
    /* same as in screen.h */
    if ((size != FRAMESIZE_96X96) &&
        (size != FRAMESIZE_QQVGA) &&
        (size != FRAMESIZE_QCIF) &&
        (size != FRAMESIZE_HQVGA) &&
        (size != FRAMESIZE_240X240) &&
        (size != FRAMESIZE_QVGA) &&
        (size != FRAMESIZE_CIF) &&
        (size != FRAMESIZE_HVGA) &&
        (size != FRAMESIZE_VGA) &&
        (size != FRAMESIZE_SVGA) &&
        (size != FRAMESIZE_XGA) &&
        (size != FRAMESIZE_HD) &&
        (size != FRAMESIZE_SXGA) &&
        (size != FRAMESIZE_UXGA) &&
        (size != FRAMESIZE_FHD) &&
        (size != FRAMESIZE_P_HD) &&
        (size != FRAMESIZE_P_3MP) &&
        (size != FRAMESIZE_QXGA) &&
        (size != FRAMESIZE_QHD) &&
        (size != FRAMESIZE_WQXGA) &&
        (size != FRAMESIZE_P_FHD) &&
        (size != FRAMESIZE_QSXGA)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Image framesize is not valid"));
    }

    s->set_framesize(s, size); 

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_framesize_obj, camera_framesize);

STATIC mp_obj_t camera_quality(mp_obj_t what){
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Quality Failed");
        return mp_const_false;
      }
    int val = mp_obj_get_int(what); // 10-63 lower number means higher quality
    s->set_quality(s, val);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_quality_obj, camera_quality);

STATIC mp_obj_t camera_contrast(mp_obj_t what){
    //acquire a frame
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Contrast Failed");
        return mp_const_false;
      }
    int val = mp_obj_get_int(what); // -2,2 (default 0). 2 highcontrast
    s->set_contrast(s, val);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_contrast_obj, camera_contrast);

STATIC mp_obj_t camera_saturation(mp_obj_t what){
    //acquire a frame
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Saturation Failed");
        return mp_const_false;
      }
    int val = mp_obj_get_int(what);
    s->set_saturation(s, val); // -2,2 (default 0). -2 grayscale
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_saturation_obj, camera_saturation);

STATIC mp_obj_t camera_brightness(mp_obj_t what){
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Brightness Failed");
        return mp_const_false;
      }
    int val = mp_obj_get_int(what);
    s->set_brightness(s, val); // -2,2 (default 0). 2 brightest
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_brightness_obj, camera_brightness);

STATIC mp_obj_t camera_speffect(mp_obj_t what){
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Special Effect Failed");
        return mp_const_false;
      }
    int val = mp_obj_get_int(what);
    s->set_special_effect(s, val); // 0-6 (default 0).
                                   // 0 - no effect
				   // 1 - negative
				   // 2 - black and white
				   // 3 - reddish
				   // 4 - greenish
				   // 5 - blue
				   // 6 - retro
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_speffect_obj, camera_speffect);

STATIC mp_obj_t camera_whitebalance(mp_obj_t what){
    sensor_t * s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "White Balance Failed");
        return mp_const_false;
      }
    int val = mp_obj_get_int(what);
    s->set_wb_mode(s, val); // 0-4 (default 0).
                                   // 0 - no effect
                                   // 1 - sunny
                                   // 2 - cloudy
                                   // 3 - office
                                   // 4 - home
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_whitebalance_obj, camera_whitebalance);

STATIC const mp_rom_map_elem_t camera_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_camera) },

    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&camera_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&camera_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_capture), MP_ROM_PTR(&camera_capture_obj) },
    { MP_ROM_QSTR(MP_QSTR_flip), MP_ROM_PTR(&camera_flip_obj) },
    { MP_ROM_QSTR(MP_QSTR_mirror), MP_ROM_PTR(&camera_mirror_obj) },
    { MP_ROM_QSTR(MP_QSTR_framesize), MP_ROM_PTR(&camera_framesize_obj) },
    { MP_ROM_QSTR(MP_QSTR_quality), MP_ROM_PTR(&camera_quality_obj) },
    { MP_ROM_QSTR(MP_QSTR_contrast), MP_ROM_PTR(&camera_contrast_obj) },
    { MP_ROM_QSTR(MP_QSTR_saturation), MP_ROM_PTR(&camera_saturation_obj) },
    { MP_ROM_QSTR(MP_QSTR_brightness), MP_ROM_PTR(&camera_brightness_obj) },
    { MP_ROM_QSTR(MP_QSTR_speffect), MP_ROM_PTR(&camera_speffect_obj) },
    { MP_ROM_QSTR(MP_QSTR_whitebalance), MP_ROM_PTR(&camera_whitebalance_obj) },

    // Constants
    { MP_ROM_QSTR(MP_QSTR_JPEG),            MP_ROM_INT(PIXFORMAT_JPEG) },
    { MP_ROM_QSTR(MP_QSTR_YUV422),          MP_ROM_INT(PIXFORMAT_YUV422) },
    { MP_ROM_QSTR(MP_QSTR_GRAYSCALE),       MP_ROM_INT(PIXFORMAT_GRAYSCALE) },
    { MP_ROM_QSTR(MP_QSTR_RGB565),          MP_ROM_INT(PIXFORMAT_RGB565) },
    
    { MP_ROM_QSTR(MP_QSTR_FRAME_96X96),     MP_ROM_INT(FRAMESIZE_96X96) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QQVGA),     MP_ROM_INT(FRAMESIZE_QQVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QCIF),      MP_ROM_INT(FRAMESIZE_QCIF) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_HQVGA),     MP_ROM_INT(FRAMESIZE_HQVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_240X240),   MP_ROM_INT(FRAMESIZE_240X240) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QVGA),      MP_ROM_INT(FRAMESIZE_QVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_CIF),       MP_ROM_INT(FRAMESIZE_CIF) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_HVGA),      MP_ROM_INT(FRAMESIZE_HVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_VGA),       MP_ROM_INT(FRAMESIZE_VGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_SVGA),      MP_ROM_INT(FRAMESIZE_SVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_XGA),       MP_ROM_INT(FRAMESIZE_XGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_HD),        MP_ROM_INT(FRAMESIZE_HD) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_SXGA),      MP_ROM_INT(FRAMESIZE_SXGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_UXGA),      MP_ROM_INT(FRAMESIZE_UXGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_FHD),       MP_ROM_INT(FRAMESIZE_FHD) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_P_HD),      MP_ROM_INT(FRAMESIZE_P_HD) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_P_3MP),     MP_ROM_INT(FRAMESIZE_P_3MP) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QXGA),      MP_ROM_INT(FRAMESIZE_QXGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QHD),       MP_ROM_INT(FRAMESIZE_QHD) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_WQXGA),     MP_ROM_INT(FRAMESIZE_WQXGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_P_FHD),     MP_ROM_INT(FRAMESIZE_P_FHD) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QSXGA),     MP_ROM_INT(FRAMESIZE_QSXGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QSXGA),     MP_ROM_INT(FRAMESIZE_QSXGA) },

    { MP_ROM_QSTR(MP_QSTR_WB_NONE),         MP_ROM_INT(WB_NONE) },
    { MP_ROM_QSTR(MP_QSTR_WB_SUNNY),        MP_ROM_INT(WB_SUNNY) },
    { MP_ROM_QSTR(MP_QSTR_WB_CLOUDY),       MP_ROM_INT(WB_CLOUDY) },
    { MP_ROM_QSTR(MP_QSTR_WB_OFFICE),       MP_ROM_INT(WB_OFFICE) },
    { MP_ROM_QSTR(MP_QSTR_WB_HOME),         MP_ROM_INT(WB_HOME) },

    { MP_ROM_QSTR(MP_QSTR_EFFECT_NONE),     MP_ROM_INT(EFFECT_NONE) },
    { MP_ROM_QSTR(MP_QSTR_EFFECT_NEG),      MP_ROM_INT(EFFECT_NEG) },
    { MP_ROM_QSTR(MP_QSTR_EFFECT_BW),       MP_ROM_INT(EFFECT_BW) },
    { MP_ROM_QSTR(MP_QSTR_EFFECT_RED),      MP_ROM_INT(EFFECT_RED) },
    { MP_ROM_QSTR(MP_QSTR_EFFECT_GREEN),    MP_ROM_INT(EFFECT_GREEN) },
    { MP_ROM_QSTR(MP_QSTR_EFFECT_BLUE),     MP_ROM_INT(EFFECT_BLUE) },
    { MP_ROM_QSTR(MP_QSTR_EFFECT_RETRO),    MP_ROM_INT(EFFECT_RETRO) },

    { MP_ROM_QSTR(MP_QSTR_XCLK_10MHz),      MP_ROM_INT(XCLK_FREQ_10MHz) },
    { MP_ROM_QSTR(MP_QSTR_XCLK_20MHz),      MP_ROM_INT(XCLK_FREQ_20MHz) },

    { MP_ROM_QSTR(MP_QSTR_DRAM),            MP_ROM_INT(CAMERA_FB_IN_DRAM) },
    { MP_ROM_QSTR(MP_QSTR_PSRAM),           MP_ROM_INT(CAMERA_FB_IN_PSRAM) },

};

STATIC MP_DEFINE_CONST_DICT(camera_module_globals, camera_module_globals_table);

const mp_obj_module_t mp_module_camera_system = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&camera_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_camera, mp_module_camera_system);


#endif