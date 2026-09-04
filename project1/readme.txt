Edge Case Handling:
1. Comprehend Is Unavailable
    In the case comprehend is unavailable we submit to our database an unknown sentiment values with neutral score 1
2. MIXED Sentiment Results
    TBD
3. Future-Dated or Backdated Press Releases
    Future dates for press releases are allowed 
4. Very Short Release (Headline Only, No Body)
    Enforce minimum body length of 20 for body text to ensure sentiment analysis works well. 
    Decided on 20 because a sentence on average is about 20 words
5. Concurrent Mutations
    if two analysis edit a press_release at the same time, then the only changes made by the person who pushed last will go through
    if a company is deleted while a new press_release is being analyzed the press release will go through since sentiment is stored seperately from 
    press release

Notes:
    Deleting a company results in deleting all associated press_releases. Necessary due to foreign key contraint between press_releases and companies
    
    Editing body_text in press_release does not incur sentiment analysis again

