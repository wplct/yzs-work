INDX( 	 �CS]           (   8   �       ~   elat                            1	    ~������[��������[��� 0      {&              { 2 F 0 1 6 ~ 1 . T M               - b 6 d d - 2 5 7 3 f d 9 c d 6 7 2 } ~ 0�   	 h R     1	    ~������[��������[��� 0      {&              { 2 F 0 1 6 ~ 1 . T M               - b 6 d d - 2 5 7 3 f d 9 c d 6 7 2 } ~ R F 3 0 b 8 7 b 1 . T M P { 2 F 0�   	 h R     1	    ~������[��������[��� 0      {&              { 2 F 0 1 6  1 . T M               1	    ~�������������������                        { 2 F 0 1 6 ~ 1 . T M P                                   { 2 F 0 1 6 ~ 1       0�   	 p Z     1	    ~������[����[����[��� 0      {&              { 2 F 0 1 6 ~ 1 . ~ T M                     1	    ~������[����[����[��� 0      {&              { 2 F 0 1 6 ~ 1 . ~ T M                         for note in note_list:
            self.assertTrue(note.priority > now_priority)
           now_priority = note.priority

    def test_base_field_enabled(self):
        """
        测试是否启用字段
        :return:
        """

        note = Note()
        note.save()

        # 检查默认值

        self.assertEqual(note.enabled, True)
        note = Note.active_objects.first()
        self.assertEqual(note.enabled, True)

        # 测试删除

        note.delete()
        note = Note.objects.first()
        self.assertEqual(note.enabled, False)
        s f.assertEqual(0, Note.active_objects.count())

        # 测试强制删除

        note.delete(real_delete=True)
        self.assertEqual(0, Note.active_objects.count())
        self.assertEqual(0, Note.objects.count())

    def test_base_field_date(self):
        """
        测试创建时间和修改时间
        :return:
        """
        create_at_start = timezone.now()
        note = Note()
        note.save()
        create_at_end = timezone.now()

        self.assertTrue(cre e_at_start <= note.created_at <= create_at_end)
        self.assertTrue(create_at_start <= note.updated_at <= create_at_end)

        updated_at_start = timezone.now()
        note.title = '1'
        note.save()
        updated_at_end = timezone.now()

        self.assertTrue(updated_at_start <= note.updated_at <= updated_at_end)

