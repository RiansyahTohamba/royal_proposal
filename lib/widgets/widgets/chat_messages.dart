import 'package:flutter/material.dart';
import 'package:royal_ai/widgets/widgets/assistance_message_widget.dart';
import 'package:royal_ai/widgets/widgets/my_message_widget.dart';

import '../../models/message.dart';
import '../../provider/chat_provider.dart';

class ChatMessages extends StatelessWidget {
  const ChatMessages({
    super.key,
    required this.scrollController,
    required this.chatProvider,
  });

  final ScrollController scrollController;
  final ChatProvider chatProvider;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: scrollController,
      itemCount: chatProvider.inChatMessages.length,
      itemBuilder: (context, index) {
        // compare with timeSent bewfore showing the list
        final message = chatProvider.inChatMessages[index];
        return message.role.name == Role.user.name
            ? MyMessageWidget(message: message)
            : AssistantMessageWidget(message: message.message.toString());
      },
    );
  }
}
