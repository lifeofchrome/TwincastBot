package com.twincast.bot.Utils.Command;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

/**
 * Created by srgood on 10/22/2016.
 */


@Retention(RetentionPolicy.RUNTIME)
public @interface Command {
    String name();
}
