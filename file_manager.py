###########################################
# File Management with the RapidMail API. #
# v. 0.2 - Alpha                          #
###########################################

import rapidmail as rm
#import pandas as pd
#import os

"""
! Section for data and file management
! under construction
TODO make this own class, either in this module or in separate
# TODO: Add database functionality
# TODO: add delta-loading, so only new entries are added, if used with database
"""


def save_mailing_stats(filename):
    mailing_list = []
    for elem in Mailings().all_mailings:
        main_stat = elem
        detail_stat = Mailing(elem['id']).mail_stats
        main_stat.update(detail_stat)
        mailing_list.append(main_stat)
    mainframe = pd.DataFrame.from_dict(mailing_list)
    return df_to_csv(mainframe, filename)


def save_recipients_stats(filename, list_id):
    recipients = Recipient(list_id).details
    mainframe = pd.DataFrame.from_dict(recipients)
    # * drop personal data columns to anonymize the dataset
    # * important for GDPR compliance
    mainframe.drop(columns=['email', 'firstname',
                   'lastname', 'title'], inplace=True)
    return df_to_csv(mainframe, filename)


def df_to_csv(dataframe, filename):
    dataframe.to_csv(os.path.join(
        config['FILE_PATH']+f"{filename}.csv"), index=False)
    return f"Finished - saved CSV to: {filename}.csv"


def main():

    filename = input("What filename do you want to save the data to? ")
    list_id = input("Which List ID to pull data from? ")
    print(f"Data from {list_id} will be saved to {filename}.csv)")
    print(save_recipients_stats(filename, list_id))


if __name__ == "__main__":
    main()
