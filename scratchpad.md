<pre>
<code>
df1 = pd.DataFrame(messages_with_detected_languages,
                   columns=["detected_lang", "detected_lang_score", "text"])
print(df1['detected_lang'].unique())
df1.loc[df1['detected_lang'] == 'uk'].sort_values('detected_lang_score') || print(item, sep=' ', end='', flush=True)
</code>
</pre>