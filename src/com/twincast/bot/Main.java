package com.twincast.bot;

import com.twincast.bot.Utils.Command.CommandInterface;
import net.dv8tion.jda.JDA;
import net.dv8tion.jda.JDABuilder;

import javax.security.auth.login.LoginException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by srgood on 10/22/2016.
 */
public class Main {
    public static String prefix = "!";
    public static JDA jda;
    public static Map<String,CommandInterface> commands = new HashMap<>();


    //register JDA
    public static void main(String args[]) {

        try {
            jda = new JDABuilder().addListener(new TwincastListener()).setBotToken("MjM5NDU5Mjc5ODgxNTAyNzQx.Cu1FuQ.bvv6Tk577Qh-Zf_6RB-F5n0F1P4").buildBlocking();
        } catch (LoginException e) {
            //TODO: handle
        } catch (InterruptedException e) {
            //TODO: handle
        }
    }

    //load commands

}
