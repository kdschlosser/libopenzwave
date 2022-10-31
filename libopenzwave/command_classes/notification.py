# -*- coding: utf-8 -*-

# **libopenzwave** is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# **libopenzwave** is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""

This file is part of the **libopenzwave** project

:platform: Unix, Windows, OSX
:license: GPL(v3)
:synopsis: COMMAND_CLASS_NOTIFICATION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Notification Command Class - Active
# Application
COMMAND_CLASS_NOTIFICATION = 0x71


# noinspection PyAbstractClass
class Notification(zwave_cmd_class.ZWaveCommandClass):
    """
    Non Interoperable Command Class

    symbol: `COMMAND_CLASS_NOTIFICATION`
    """
    class_id = COMMAND_CLASS_NOTIFICATION
    class_desc = 'COMMAND_CLASS_NOTIFICATION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        event_start = 0
        event_smoke_alarm = 1
        event_carbon_monoxide = 2
        event_carbon_dioxide = 3
        event_heat = 4
        event_water = 5
        event_access_control = 6
        event_home_security = 7
        event_power_management = 8
        event_system = 9
        event_emergency = 10
        event_clock = 11
        event_appliance = 12
        event_home_health = 13
        event_siren = 14
        event_water_valve = 15
        event_weather = 16
        event_irrigation = 17
        event_gas = 18
        event_19 = 19
        event_20 = 20
        event_21 = 21
        event_22 = 22
        event_23 = 23
        event_24 = 24
        event_25 = 25
        event_26 = 26
        event_27 = 27
        event_28 = 28
        event_29 = 29
        event_30 = 30
        event_31 = 31
        event_32 = 32
        event_33 = 33
        event_34 = 34
        event_35 = 35
        event_36 = 36
        event_37 = 37
        event_38 = 38
        event_39 = 39
        event_40 = 40
        event_41 = 41
        event_42 = 42
        event_43 = 43
        event_44 = 44
        event_45 = 45
        event_46 = 46
        event_47 = 47
        event_48 = 48
        event_49 = 49
        event_50 = 50
        event_51 = 51
        event_52 = 52
        event_53 = 53
        event_54 = 54
        event_55 = 55
        event_56 = 56
        event_57 = 57
        event_58 = 58
        event_59 = 59
        event_60 = 60
        event_61 = 61
        event_62 = 62
        event_63 = 63
        event_64 = 64
        event_65 = 65
        event_66 = 66
        event_67 = 67
        event_68 = 68
        event_69 = 69
        event_70 = 70
        event_71 = 71
        event_72 = 72
        event_73 = 73
        event_74 = 74
        event_75 = 75
        event_76 = 76
        event_77 = 77
        event_78 = 78
        event_79 = 79
        event_80 = 80
        event_81 = 81
        event_82 = 82
        event_83 = 83
        event_84 = 84
        event_85 = 85
        event_86 = 86
        event_87 = 87
        event_88 = 88
        event_89 = 89
        event_90 = 90
        event_91 = 91
        event_92 = 92
        event_93 = 93
        event_94 = 94
        event_95 = 95
        event_96 = 96
        event_97 = 97
        event_98 = 98
        event_99 = 99
        event_100 = 100
        event_101 = 101
        event_102 = 102
        event_103 = 103
        event_104 = 104
        event_105 = 105
        event_106 = 106
        event_107 = 107
        event_108 = 108
        event_109 = 109
        event_110 = 110
        event_111 = 111
        event_112 = 112
        event_113 = 113
        event_114 = 114
        event_115 = 115
        event_116 = 116
        event_117 = 117
        event_118 = 118
        event_119 = 119
        event_120 = 120
        event_121 = 121
        event_122 = 122
        event_123 = 123
        event_124 = 124
        event_125 = 125
        event_126 = 126
        event_127 = 127
        event_128 = 128
        event_129 = 129
        event_130 = 130
        event_131 = 131
        event_132 = 132
        event_133 = 133
        event_134 = 134
        event_135 = 135
        event_136 = 136
        event_137 = 137
        event_138 = 138
        event_139 = 139
        event_140 = 140
        event_141 = 141
        event_142 = 142
        event_143 = 143
        event_144 = 144
        event_145 = 145
        event_146 = 146
        event_147 = 147
        event_148 = 148
        event_149 = 149
        event_150 = 150
        event_151 = 151
        event_152 = 152
        event_153 = 153
        event_154 = 154
        event_155 = 155
        event_156 = 156
        event_157 = 157
        event_158 = 158
        event_159 = 159
        event_160 = 160
        event_161 = 161
        event_162 = 162
        event_163 = 163
        event_164 = 164
        event_165 = 165
        event_166 = 166
        event_167 = 167
        event_168 = 168
        event_169 = 169
        event_170 = 170
        event_171 = 171
        event_172 = 172
        event_173 = 173
        event_174 = 174
        event_175 = 175
        event_176 = 176
        event_177 = 177
        event_178 = 178
        event_179 = 179
        event_180 = 180
        event_181 = 181
        event_182 = 182
        event_183 = 183
        event_184 = 184
        event_185 = 185
        event_186 = 186
        event_187 = 187
        event_188 = 188
        event_189 = 189
        event_190 = 190
        event_191 = 191
        event_192 = 192
        event_193 = 193
        event_194 = 194
        event_195 = 195
        event_196 = 196
        event_197 = 197
        event_198 = 198
        event_199 = 199
        event_200 = 200
        event_201 = 201
        event_202 = 202
        event_203 = 203
        event_204 = 204
        event_205 = 205
        event_206 = 206
        event_207 = 207
        event_208 = 208
        event_209 = 209
        event_210 = 210
        event_211 = 211
        event_212 = 212
        event_213 = 213
        event_214 = 214
        event_215 = 215
        event_216 = 216
        event_217 = 217
        event_218 = 218
        event_219 = 219
        event_220 = 220
        event_221 = 221
        event_222 = 222
        event_223 = 223
        event_224 = 224
        event_225 = 225
        event_226 = 226
        event_227 = 227
        event_228 = 228
        event_229 = 229
        event_230 = 230
        event_231 = 231
        event_232 = 232
        event_233 = 233
        event_234 = 234
        event_235 = 235
        event_236 = 236
        event_237 = 237
        event_238 = 238
        event_239 = 239
        event_240 = 240
        event_241 = 241
        event_242 = 242
        event_243 = 243
        event_244 = 244
        event_245 = 245
        event_246 = 246
        event_247 = 247
        event_248 = 248
        event_249 = 249
        event_250 = 250
        event_251 = 251
        event_252 = 252
        event_253 = 253
        event_254 = 254
        event_255 = 255
        param_previous_event = 256
        param_location = 257
        param_result = 258
        param_threshold = 259
        param_usercode = 260
        param_261 = 261
        param_progress = 262
        param_mode = 263
        param_obstruction = 264
        param_sensor_id = 265
        param_error_code = 266
        param_duration = 267
        param_pollution_level = 268
        param_status = 269
        param_schedule_id = 270
        param_valve_table_id = 271
        param_272 = 272
        param_273 = 273
        param_274 = 274
        param_275 = 275
        param_276 = 276
        param_277 = 277
        param_278 = 278
        param_279 = 279
        param_280 = 280
        param_281 = 281
        param_282 = 282
        param_283 = 283
        param_284 = 284
        param_285 = 285
        param_286 = 286
        param_287 = 287
        param_288 = 288
        param_289 = 289
        param_290 = 290
        param_291 = 291
        param_292 = 292
        param_293 = 293
        param_294 = 294
        param_295 = 295
        param_296 = 296
        param_297 = 297
        param_298 = 298
        param_299 = 299
        param_300 = 300
        param_301 = 301
        param_302 = 302
        param_303 = 303
        param_304 = 304
        param_305 = 305
        param_306 = 306
        param_307 = 307
        param_308 = 308
        param_309 = 309
        param_310 = 310
        param_311 = 311
        param_312 = 312
        param_313 = 313
        param_314 = 314
        param_315 = 315
        param_316 = 316
        param_317 = 317
        param_318 = 318
        param_319 = 319
        param_320 = 320
        param_321 = 321
        param_322 = 322
        param_323 = 323
        param_324 = 324
        param_325 = 325
        param_326 = 326
        param_327 = 327
        param_328 = 328
        param_329 = 329
        param_330 = 330
        param_331 = 331
        param_332 = 332
        param_333 = 333
        param_334 = 334
        param_335 = 335
        param_336 = 336
        param_337 = 337
        param_338 = 338
        param_339 = 339
        param_340 = 340
        param_341 = 341
        param_342 = 342
        param_343 = 343
        param_344 = 344
        param_345 = 345
        param_346 = 346
        param_347 = 347
        param_348 = 348
        param_349 = 349
        param_350 = 350
        param_351 = 351
        param_352 = 352
        param_353 = 353
        param_354 = 354
        param_355 = 355
        param_356 = 356
        param_357 = 357
        param_358 = 358
        param_359 = 359
        param_360 = 360
        param_361 = 361
        param_362 = 362
        param_363 = 363
        param_364 = 364
        param_365 = 365
        param_366 = 366
        param_367 = 367
        param_368 = 368
        param_369 = 369
        param_370 = 370
        param_371 = 371
        param_372 = 372
        param_373 = 373
        param_374 = 374
        param_375 = 375
        param_376 = 376
        param_377 = 377
        param_378 = 378
        param_379 = 379
        param_380 = 380
        param_381 = 381
        param_382 = 382
        param_383 = 383
        param_384 = 384
        param_385 = 385
        param_386 = 386
        param_387 = 387
        param_388 = 388
        param_389 = 389
        param_390 = 390
        param_391 = 391
        param_392 = 392
        param_393 = 393
        param_394 = 394
        param_395 = 395
        param_396 = 396
        param_397 = 397
        param_398 = 398
        param_399 = 399
        param_400 = 400
        param_401 = 401
        param_402 = 402
        param_403 = 403
        param_404 = 404
        param_405 = 405
        param_406 = 406
        param_407 = 407
        param_408 = 408
        param_409 = 409
        param_410 = 410
        param_411 = 411
        param_412 = 412
        param_413 = 413
        param_414 = 414
        param_415 = 415
        param_416 = 416
        param_417 = 417
        param_418 = 418
        param_419 = 419
        param_420 = 420
        param_421 = 421
        param_422 = 422
        param_423 = 423
        param_424 = 424
        param_425 = 425
        param_426 = 426
        param_427 = 427
        param_428 = 428
        param_429 = 429
        param_430 = 430
        param_431 = 431
        param_432 = 432
        param_433 = 433
        param_434 = 434
        param_435 = 435
        param_436 = 436
        param_437 = 437
        param_438 = 438
        param_439 = 439
        param_440 = 440
        param_441 = 441
        param_442 = 442
        param_443 = 443
        param_444 = 444
        param_445 = 445
        param_446 = 446
        param_447 = 447
        param_448 = 448
        param_449 = 449
        param_450 = 450
        param_451 = 451
        param_452 = 452
        param_453 = 453
        param_454 = 454
        param_455 = 455
        param_456 = 456
        param_457 = 457
        param_458 = 458
        param_459 = 459
        param_460 = 460
        param_461 = 461
        param_462 = 462
        param_463 = 463
        param_464 = 464
        param_465 = 465
        param_466 = 466
        param_467 = 467
        param_468 = 468
        param_469 = 469
        param_470 = 470
        param_471 = 471
        param_472 = 472
        param_473 = 473
        param_474 = 474
        param_475 = 475
        param_476 = 476
        param_477 = 477
        param_478 = 478
        param_479 = 479
        param_480 = 480
        param_481 = 481
        param_482 = 482
        param_483 = 483
        param_484 = 484
        param_485 = 485
        param_486 = 486
        param_487 = 487
        param_488 = 488
        param_489 = 489
        param_490 = 490
        param_491 = 491
        param_492 = 492
        param_493 = 493
        param_494 = 494
        param_495 = 495
        param_496 = 496
        param_497 = 497
        param_498 = 498
        param_499 = 499
        param_500 = 500
        param_501 = 501
        param_502 = 502
        param_503 = 503
        param_504 = 504
        param_505 = 505
        param_506 = 506
        param_507 = 507
        param_508 = 508
        param_509 = 509
        param_510 = 510
        param_511 = 511
        type_v1 = 512
        level_v1 = 513
        auto_clear_events = 514

    @property
    def notifications(self):
        """
        :rtype: Any
        """
        res = {}

        for i in range(1, 255):
            for key, value in Notification.ValueIndexes.__dict__.items():
                if value == i:
                    res[key] = getattr(self.values, key).data
        return res

    @property
    def notification_level(self):
        """
        :rtype: Any
        """
        return self.values.level_v1.data

    @property
    def notification_type(self):
        """
        :rtype: Any
        """
        return self.values.type_v1.data

    @property
    def notification_previous_event(self):
        """
        :rtype: Any
        """
        return self.values.param_previous_event.data

    @property
    def notification_location(self):
        """
        :rtype: Any
        """
        return self.values.param_location.data

    @property
    def notification_result(self):
        """
        :rtype: Any
        """
        return self.values.param_result.data

    @property
    def notification_threshold(self):
        """
        :rtype: Any
        """
        return self.values.param_threshold.data

    @property
    def notification_user_code(self):
        """
        :rtype: Any
        """
        return self.values.param_user_code.data

    @property
    def notification_progress(self):
        """
        :rtype: Any
        """
        return self.values.param_progress.data

    @property
    def notification_mode(self):
        """
        :rtype: Any
        """
        return self.values.param_mode.data

    @property
    def notification_obstruction(self):
        """
        :rtype: Any
        """
        return self.values.param_obstruction.data

    @property
    def notification_sensor_id(self):
        """
        :rtype: Any
        """
        return self.values.param_sensor_id.data

    @property
    def notification_error_code(self):
        """
        :rtype: Any
        """
        return self.values.param_error_code.data

    @property
    def notification_duration(self):
        """
        :rtype: Any
        """
        return self.values.param_duration.data

    @property
    def notification_pollution_level(self):
        """
        :rtype: Any
        """
        return self.values.param_pollution_level.data

    @property
    def notification_status(self):
        """
        :rtype: Any
        """
        return self.values.param_status.data

    @property
    def notification_schedule_id(self):
        """
        :rtype: Any
        """
        return self.values.param_schedule_id.data

    @property
    def notification_valve_table_id(self):
        """
        :rtype: Any
        """
        return self.values.param_valve_table_id.data
