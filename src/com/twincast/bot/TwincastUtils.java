package com.twincast.bot;

import net.dv8tion.jda.entities.Message;

/**
 * Created by srgood on 10/22/2016.
 */
public class TwincastUtils {

    public static boolean shouldHandle(Message message) {
        return message.getContent().startsWith(Main.prefix) || message.getMentionedUsers().contains(Main.jda.getSelfInfo());
    }

}
