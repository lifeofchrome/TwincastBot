package com.twincast.bot;

import net.dv8tion.jda.events.message.guild.GuildMessageReceivedEvent;
import net.dv8tion.jda.hooks.ListenerAdapter;
import static com.twincast.bot.TwincastUtils.*;

/**
 * Created by srgood on 10/22/2016.
 */
public class TwincastListener extends ListenerAdapter {

    @Override
    public void onGuildMessageReceived(GuildMessageReceivedEvent event) {
        if(shouldHandle(event.getMessage())) {

        }
    }
}
