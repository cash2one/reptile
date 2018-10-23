#!/usr/bin/env python
# encoding: utf-8
#   @file: qttnews.py
#   @Created by shucheng.qu on 2018/10/10
import json
import time

from db.mysql import getdb, closedb
from db.newsdb import save_db
import requests
from lxml import etree

from newreptile.utils.dirs import makedirs

redian = 'https://api.1sapp.com/content/getListV2?qdata=MUI3NUNDRTU0QzhFQTlDNDYyNzlFREIwQzNCQjEwRTkuY0dGeVlXMGZNVGM0UkVNME5Ea3RNREEwUlMwME5rRTBMVUl5TmtZdE1EY3hORGswUWtGRk5EaEdIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS4iEz20qVovWTl5wKsVnf%2BFOSBpaB3CVcYakZ5vW9uaz7iTmhmX6fRi05p/R%2B9qLvqZ2Qrix11lvFW/XKxuthVqhjD366HP6rcIgCYcbhihGpxhMYPLk/7n2t6fLAcnCBe3sBFFtJFVkQJy9ihUFAT61GJax7wOmQxBKhHF/ItuIDjdIBZxefuJ/iml6ZgyrGT5uVgpeWJN%2BxrB264QnUdNsrfa3saaoERd4K86Zs3X21olUNB5nGFOOIctlhDvHbHtX57siTwjMOHrqxo/EuPjivyKeEfPf3H8EAgMPMGPrluLpnPIv/Re2hlH/UWlKQ2iQC70wg4Uda%2BVrQFLUCZ0SyxjE0aX5VFkK0/mJYFZwXQ8LXRpJA7ybJ/v7cZ5QC1e/4jzR1nF3BpPuE52a93L/TiKH/oCIyzqej7hWHryYDmm7xE1tHXWQ3Pk5lUFbiNeX5LdlrUjt9cm6Sl6MFllYAGnN9k3P%2BzegOHqgvEAfJmfj%2Bu0KwSN9U4A9Afvd2idgjO7qChH9K9Eku5JBKT4SZtJKcHuHmwhYcSq8JupS1oLaGt/9KY3ElBcrPhTlCXQe0/fZVQVtsP/itRMV4/NoA/fsM/55QrTHaaFI0eGHVAzKO36u%2B/cJQiN7ai8chAZUjKLmpeEwB5dEdte4OvtihkZIN4WSWqGpWUi2fr1mlideYyWsUGvdT6ZqDS8Gc8hlX5DgN6CTtq2%2Bjty0My9hrG3RULPO2TvFKR6AyMzGxMryekRkZuYVZVELmKAiZT%2B8lSs/mH9AHx6%2BFBd30BGQeTCIIZ9LUmMQNSuodkh8iY%3D'
yule ='https://api.1sapp.com/content/getListV2?qdata=ODVBQ0U1QkZCOTY1NTlEMzIyMDg5RjA2QkE5NTcyREEuY0dGeVlXMGZORGN4UTBKR1JVRXRNVEV3TXkwME1rUkZMVGxFUWtZdFJFVXhOekpHUmpjMU5FWTJIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS6/4YcIC50Pd1t2iorT1cc0OlAz9Knz6kYjBZfrsbDywk2Y2qKRORUKGN258Npvk3OzlQMOEdc812ma7VlgiauLHyU1YKZipijL2tfdM7N77hc/3TiJFFS83Sj53ptyZa2XxVNGsRilum/A4FQFA3AFmLy2sw4BzUFBuhRfi6RQlNLPiPgbGgcIg/24PsnDr/s/oz6PQnZFVZmKQAoYIhJfenPtF1t/Mz/KK1mbr0SrpAs%2BGYpa5bm3QD4CzRqVxqB%2BISt0XfLjnzSfnEMpHPkniDIKJ05gdCEiDvf1ZAKa7uYj4oO7efwgw7c8DsfglAbiH%2BFyXyY5G/crneR179KHRRhEaVM0sZeoPRt6GmaXk7kbrE4q%2Bus%2BexfVJxBalm4aaHFmgXDtHWHz66Mjcv93o6zPKzx6xdr9zr/AtnjWBga6f89gLYcc5HwLZBeGnHNzgdSbqMhC%2B3JS95m7ltv3MYAb8X3pWEhS3AS9g1SWYsV5CdwNwy0rMn80mknz%2BJ0UjkzSqU%2By0nMCxqSNqD67ul9tdhsoQOqm01Vufkh5OsOQpfVniWjpbRjMLBpHNXoyX7cWsYhNvaq%2Bpl6pejPb2vmWpBZN64yonf6UZMkZGzfTv2qKA7nMQ7%2BAS4MLFuEhPpagXG9r58cwhum04pfAXfj2Oaj1ARRURpVtNkGR5VlADSuNhXjzxOGMMkYM%2By6j2Y5CHU/k9u3rn8hkR3MB5LA4ubRJnIRi28HhU4T38EdmEWEactcI08RpJ38Gys9tyA5aJdndKPR9yiuTpKbK1bWz73wWvjoanTTOSlKnMoA%3D'
keji = 'https://api.1sapp.com/content/getListV2?qdata=NkVFNDRBNDA5MEMwNDYyMTUxRkZCRjgyOEE0OUM1QjMuY0dGeVlXMGZOemxDTnpnM1JrWXRRelUzUlMwMFFUZENMVGswUmtNdE5UazFNMFJCTVRjeVJrWTNIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS6HKyIsY21JtM5jHYtaLJguHRAxFLz%2BwrAF6x1QU%2B54CWxVnZF82WWhqabSIrI38qdScrM5VwREXhQ9N4ueq779R2MBJvyZLjDp1dfwWRlKyLTw8/jmqsu3E9QB%2BSMTYNNZ8JwSk1%2BsiL4cQkbN4S0btN51O0GPg3sF5vNjL/uVpPGtrEnVA9EnvUQISxRpj6WKH7Y1ZmoyGaqZLf3HAwx3qXH1OwC4mSYSwK0GHke/2XLcsFqXNjnZ9JNt/buVSrvBc0GmlcYNBLHG9pE7Rk1ZdQDjrQM3eFaeZ2GF%2B9Niuy/tgJfbZ%2Bxiq5ksJjjX%2ByA6b9HmFum8YN3uKZ8ocjKkJbfMPHTkVpI4d6xLi780G8t6zprc0/%2BuMhhEfcQEkYpC0yqUgs94bKs7z2MeKFhyuNvIN/MAPMWByfgGQxY7fyjLWHW4TMNI17EYC5HojoLeZ9ba5Z4ik2E7s1IU1C%2BsewdP53azNwx%2B%2B%2BOdQPbuATjX5lUh6MmJqVcKv/Y2Mt34DIQT3KlxX%2BmVlREBmXQmMGOOzuzHXdNLOwcHNRdaZjVI1rfdDnO8IePmm8Neo7cuoJhxjYa2AcaiYZQRLTkgfpp/aq3FDDef45MhToRhHpGOhNZksVNEpE3hO/y8O8CKjmnDqaSA2aEoxG2xMsONtUbx0qiiokgpK7cvcNvQgG6cGoN9UBfXv3A6jNbrx2E9AxyLcpZ4LmF26NFfc2GMszuVfIb0FE%2BU7yChtOQ6m86ovcPsTKXi7KWV0Ztw/Yk/c5dqHmTDzWtJGxwRyXgqCQ%3D%3D'
shenghuo = 'https://api.1sapp.com/content/getListV2?qdata=MDJGRUFGNEU5Q0VERTUyREU3NzQ1OEMzMzgyMDA0Q0UuY0dGeVlXMGZNVUl5TTBRMFFqWXRSVUV5UVMwME5UQkNMVGxGTVVFdE4wSkdOREZETlVKRlJEQXhIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS42tYuiec/0j0/mtXVFYHAsuHnSO1uXjYxrIatNrz%2BjFP%2BYmUcyjHeWE458W7VCKUlsRgEt4QTXp74KyX6wni%2BjSb5rP%2Bu10IFwtkVql9BgMrD%2B1kJrw4TWRSpj2LQBfLgmC%2Becg5p%2BTMKBNttyUF0lGU36mBcXdBLnWxpxOXTMvKvLWKA4P9ZcKgniPcWLIbPhNLVB/VFWNctBG4OoVA9lrAhCWTv041JrQQrgSS175s/oEhcc4pGEZuE5DVDdng/ulBj/hxB1fgMt8A22BaRjmOV5IM0QmStlxst99eqOf/2xCk%2B1flIhifbLncrKmO1/cwqSHSmHNTgMqlglNeCxDW/dKsHM%2B0lH/6dACe5Vr1iIK05VRXIxuYDUg6AykNX%2B6TmGA8frdv2JuyFuIDRqlEHYVvtjg/muMVBcZyQmRQX7DwvlbRONhIJqp4e5bpdH%2Bt9btwQQnfE/XksgyGknE3ieCvebM%2BSffRrYlQ0v45Ylg423tgVv2ZYK8HHBuwaBlqzXS%2BwSDEvVMLbx2OXkpcc4g8tic%2BS2tEt8vmdRRmBjhE4aL1ZRVHBSA8AQPafQunqnlBJG66SyH8d1kjutfwWfSiR8zgx0i6wS4A5ZnfgsdHexaxs5axeQgOep1p2TocfaGb8%2BlM0YFF5/3aqZwhxfBtlygSD7XxqyyKnX/L3NrRAVgzay7R5uQ1TjTHp0z2MykFt7mRbzC/%2BqRgCVvyDoYCGbvWdPOqcSDRnNSSWUSFLH%2BJFNeceQpUABLOT6HZ2PFN0ROCaKVoj%2BtrficA%3D%3D'
qiche = 'https://api.1sapp.com/content/getListV2?qdata=RkRBQkNBRjczNzYxMkNGMDBDNTcyREY1MjdDNDA4NkQuY0dGeVlXMGZNa0pDUkVRek1qa3RNVFV6TnkwME5EWTJMVUk1TmpBdFJqUkVRekU1T0RJMFJEZERIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS6Tgn%2BefQiuxPVwrQWJvR/hRWnKgbtITqHDQcShwiFf0Gf%2BLpGnfPirOaY8kIFdKF/dTRmmlWqNUu8cSxlk8ayTtvnnHwzJkphS5383jELsJpd7ESUsnEGn%2BotXFKwRTEaRY/oqMc/VOY9Ktj84UZ51%2BK8mz8mm/qzZK2bXp69pPsdfCKMtGzFmmESBrxdXybEQfjaAdemLRx41xhsVYfguGAXHSctrirODTUK83EKzKXAv7cbloJDlzqysRqTMdv46ZXCZL/nOFmjzQquRtEWqxVtzxvr2%2BPMWMwYjSL0vabXQubZCTTerY1Zp0OIEpjhQg0rTwHM034eIIQMb7jCqdAhsFruc6mKVd6RT4F2jHWEuMHco/ypFK9f/r74jKtPSutS2MFEioNlm3Mnsc8VnwpdG16hOTJq8Rny%2BmJMe9czV8tK4cSg7w/3sApWctGdmBOQpzowz/EDh77kKFGA/HfainnqpCWLZl2izP3NNu0Gsx1Pyu6F/0FO421DuVjdAy3xfCSJWAquRzN/vDlIQiFxQVZZwU0JgpBlD0M3W6y%2BIBYZRsCEfSo4VZs6zwPSSL1LJf8QqTMfBEPMAKGn1anbTpJ38v7pJYbxNlcBhrZatM3NT/4QUj7DOyctvQy/Ubb/kuZBiWh4DwDOqwg4UFNsZs92RBRaC8cud33PQ0IiQsNiSiFYRJzoq85W%2BxrabIAkAZB9MSCHNBW6I/X/N7aWI53/OdgbHNh/AKKURKGOtMRIlDNf6oqa%2Bmu5uRGKRK9XyOH24Z00xHNwW6Dsx2Q%3D%3D'
tiyu = 'https://api.1sapp.com/content/getListV2?qdata=MDFGNTc3OTJCOTFDM0JCNzM4QTQzQzZBNUM2NDdDNDQuY0dGeVlXMGZRVGM0TlRSRk5FRXRPRFl4TlMwME1FUkVMVGs0UVRrdFF6aENOVEJCTkVWQk16VXpIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS5I026b7I2/Vqle5EHGXmUG/S0YVezvBDJ4zg3frmmcN8SuTUL0aHTXCRjvxHEajfE6Ub527TsjRUquAawvDPffoeCgT5OzI3XNbisYvMCOjjL9WgEGSgr72oRSufn0jazRabYS3wHE8FMtsMh3d78kuAuGJBCqlvyZn7jN/iE/MGs%2Bgr1%2BH/vlpwMiAMdILlO1Y38JqDAwBMtl4lBcL/yiFVkth90wJM4Sr9OdA1vzlQMN0yg7bD4kyK/XR9X6xByxZSLpk0uP5kFK9lB8c%2BP1CzKEmG5bhYQbixiV6LCDyuEIwOHBrnBSJtm/5gjOkTi9Ulu6ZaUlMEsa5CEuEWoaWOttajFzTpnl5GLUcUfrLeTLMLtlBhY0TCBP%2BzGpqeyY0y9UilLDN/5noK4Nzj14SvTUSeFNyD89WBneri8BYVlUnESy%2BCn4mATPOC1lRolf8htBNh6Mzpf49Tq4omFQLhw83zw9Mmwg7XvsP%2BMrV8jxAwuyiIf1Vc6QXuFx31diymb%2BAWIbI2Wrlhx3ONx/VagUBMw2ySxQqDcWB84epUMpIjPuFnSuLnD8o1YdhiayA8o4SnZCimJyJ3IdjGA2MdFZfrKaOrC1dXeZ8RbnaoMnsbl7bMflUEPjLK0rvjdRV52Huyh%2Ba9bUf/l2VRA%2B1axuca2ME0%2BatlWrITxhR5QUeIiYmehL/ln7nP/SDnP9rKTpJvGpIfX4Su4lprv8nlu3DRYKafR3VZbXC8o5zB0XvGVChxECdwHG6/xDpd6%2BHV47E8FmoDkkf9RV1CnUlg%3D%3D'
junshi = 'https://api.1sapp.com/content/getListV2?qdata=QzZFNkNBRkMyNkM4NDgwMTg1NzFDQ0Q4RjZCQjc1MTkuY0dGeVlXMGZNakZGTlRSR01UUXROalZETlMwME9EVXlMVGd6TmtVdE4wSTJORVZEUWpVM05rSXdIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS4dt3ePy2hNPyjDb%2BRhFwyY8ZKI1KXRJve99qVNgfI5Q3n1RinSzi6KamQw/NNan6RDZkqG6S1G0lWx9%2BiDMppHfcTsXfFsfRlqREOl1Obajq6UokgA8gS66axcEa57TDtYIhGIKpsvjY4uFHVz%2Bs3fpyBnQvvUHFnjSfNApXm0PEz79Y8VM8pTsg0KsGH7pn2yj4Z5/p53FulqcVeFaFDqEnfxil/bJeuaTMeVeG%2BIfUT0b60DUN95Ryx68HkxU1W8WRPp8k8mM7WUMHB56w6wd6HjFFpUuq3o9jtithO9lFju4zOk1P6DZg3M1ahCykfpAwQls8pUj2aHFDQ6Hgo0stUgxP44OlmQW%2BQsjPgV5qb76U0yxdCzL2zDCszSJdzH3OBx5JZ1CSEw2xwxmqRnDGssyBPYzExwmEWMPXALTmCSDszGDHDrLlKeLIQ0icYHnEA/TNSrdphrR%2BFwnSWc/CfTNilNErN0X81TotkN5B5KGSco%2BfTmqFOrNcVKYpZgPQetqSu8pT%2BCHJe%2BFX/jl21qqFyzVWwITsd9YqNgmFgzDvEjqryg7Ua0mCFAJ7OuJkb3ZK%2BzW8k3tWhkEfHV8dWKkeCOgMsszfOtsYOIaeffXPDcRKT2SK1JWTeJXTkPHGvevDfhDttldCM1TWKgRjc/KgR9QXdDTq/SUmr91jyLGm36EzX3UAB//T%2BAk5s4o%2BMscBasCPdwK8BQJKfFlmfEKPKmf7Vyo7Uk0FYeC%2BTX1gxBH6FWlyF8BjSu0rf4H4sY%2B0UCijxZcHYRT4h%2Bzw%3D%3D'
lishi = 'https://api.1sapp.com/content/getListV2?qdata=MjYxN0Q4MjUwMkY0NUJGRjY3RDdBQjBGRDEyQUI2OEUuY0dGeVlXMGZNVFpDTlRCQlF6QXRNRGN4TmkwME1rWXlMVGs0UVRBdE1qQXdRMFZGTnpkRk5qUkdIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS51zji2D0tKdejj1ZMVolzVesXzSXmnkUwtdhrVdMLuI1kWgEiFPfTKC5pcM3Er7GP1AQWqB5h6Ht8RpVHNvYdVeDG0UZXc8gUFLm8tLIhOTr64o2bq56BQ7p6/cDkOWdAhwYehfKoEkUFVfJFWFm87mIiqUQHOyl9peqleO/P9cYIMcj/iNp/WluNtOLMR0HOut3L1lufxQZt5/5nO9byThaoVEV/w1u4w7gk5d3uS1f%2B48YU6XU48I1a%2BJCRFZOYD7JPMJMUzoDvxt4ppZH1QjlgtHj%2BSx2JaBHbqnpmjwxr5xlnFUu9DgG/G5A%2BNnUZj7HiuZ55RnUC6o6rWarwlPLHG3s6EDYaN3LVqhDTFuuNWS/BjmBOBbbRKKIaatRlITfBIGCRbwm9RZSGr9YbIbDK0NBSUS61vbYWB6YNcNeRIEV35wd36Wk76XmMfpv5%2BezslRFfIb/RyP2KzMZ5gQNU8Zxt2uNJTD20JrpNXWktP9YMc3cieAQFXihvPcB73Yzk7BzArJ%2BScnytdWOJMhDxWZawDkNlFBuqfYtjiP6XMcxDGjshi1zfTIcSAArFUKUfUm/6dBZgFjKqF0XQ2/SaDr4gGhH%2BCWr7KAnBdYbeIgiQSoFI/xCD/15TecJI5R%2BwVzhZjsAjwg9h0T6nJ/x5LLmtq1KzNfxClwOf4CQQgNIimmjf8CsKPBC/sF7iYwL1QBNSV4edpaNdzR5OB7OLoqQPqu96zFMGw3e5Lf8Zr6YHiugALpyVbBPWCoeRyZmYBlmh2Zb7WpAqveSOMDQ%3D%3D'
sannong = 'https://api.1sapp.com/content/getListV2?qdata=MEJDOUY5MjRBNUIxMDM5MjZGMTQ4NUJCRTlBOTg2RTYuY0dGeVlXMGZNa013UkVNelJVRXRSakEwTkMwMFJEa3pMVGs0UmpFdE1UWTNOa1V6UmpZME9UTTRIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS52xFFU2lCxm91ovw8ewGRpisszMGf1Pmmq1wV2lBz8iYGTY6lTy28B%2BwvTIkOKnnDG4dNO3HB2NK13t44VLFKsyKSkbSHg7MQvspeJntifTCM/17omm52Z1/l%2BCAU1mAZYL7nZnHvORdQe8ACflC5SUd%2BBh9FSf/%2BwekSFxYac4MvRhHLtyZRWXImbFyuD27a2%2BaT5M/OtPDaKJxfgY2fBFpxXWtKYuoSjNgxMtuB7DrE20Q6HkSce6g/DfeT16DjP8yc2sFYltp8LyJ9/4EyJSqkV3lHC5fRSyx8fhX54Y13ut0EAoor/GkX/%2BG08e/tJfqaZ9ullO8sNDoaiREo6SXey3a0vKDbgP2JThePbkdeO7FpAxdG12zEyPaWlzezsP8SsZXRhVpWYUQX0JvxTYiWu7IV3G9ReXCa9wTWvY6oA%2Bw5YaxetxcCx4eSqv%2BlvbD2gFI6aEmn78QzR9giN6P8%2B0wVURncteFjFwy4vgyGOCCcLInhb8iTQY%2BCEFCKnWPFauIMJAstfkNB9lgqUEX1u0cGCVquluJ5JML8obSAyWnmsUDGIjy0AkQRNz8e9CYmkuJ19qmlOA8%2BAggmnJQ5Ajn9%2BVtpTxLhFR/U4VSkSFt8SHR1GQ1iYCg/cOeoaq%2BmfOuHtuTqXKfykYvbOI8r7ZyAV%2Bj2KhD2s4ip9v0EF3nzwWiBh6R2HLKtbIqQABpz%2B47cRnVigy4thKjVkCiIOM2dV5okaOoPKxClUp2sQBENn1u3FhfrAqB%2BVb2YeCwfAUYTZKhm40wI%2Bi9VH0w%3D%3D'
youxi = 'https://api.1sapp.com/content/getListV2?qdata=RjA5RTBGNzExNjI3ODA0NDU2OEEzMUMwNjVERUY5NzkuY0dGeVlXMGZNVE5HTVVJd09EUXRRVFEyUWkwME16WXdMVGd6UWtVdE1VSTRNVU0zTmpNM1JqUTFIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS411Q3A5hwOqx91wOqh8gf2ULOgaqGziotxmYoPvuqPW3k%2BNK1P98usUrSEPgNj7ByQe8zXZqRibOTU7OzDxUuOTHQ84GO8mrZnvd14JT9eOo0LNJPabT1kYvwoGg0FZThaSUVydQjLtipwWGwamqGgSH/6iaHGfkBbSnYWIBhBpuXCo5F39neZq1XbathZHYVFKQnugk5%2BCouu3ug9HMM0B6q2MmAgHjwG6fgBOUE7lxiWd7h4GmTtYjr0hCeOyCG%2BYa4jt3q9oR0ahWdMrQc5ulRbjOHc3u2oAQ1vPnNROpjbU86u4W1sYnjrSDzdvMZn5%2BlabMxaJ5WIX0F/GZx211aXjwS1O48ki7RZaVxLS6fz7CjNx2GRRmK/QHCKjyM87zi/G6p0WsYhrheKluHvKPvdJ8XPIxxD4bPxzq8nWI1/dWIDj9Qw680HmWppKwI7IoSf%2B%2BS41rccaM44v1%2BeJ19sOUD/snEeIG0AvFCJznurqws77UT37cVw2rGzW6jq4a21f%2BQ2vaK0%2BtKWfRAjQx63a3NUAXHJJ4KUmQyHRQolk/%2BgIvjjHm1eCwS6tbE2OpnD4uFvPFiMWrWO%2BxQdYljzlTIAElLbiqOfJ6LRL4lavsSeHDXZo/9Oj6wB0dDB4RUKpxY5c0BgT3t4IsaneKTgZaL/r4w1Te76R9nWOv878PGyh2sOUOFArT5RlLW3HhXDRuXP9zGnpDCzcjnT6eyrPp7YtCCByuYaH%2BB9dXWCXzG93IF6ze/%2BfPFZwLQyHvlHGZGPg6FsJLWRerkYWg%3D%3D'
xinliceshi = 'https://api.1sapp.com/content/getListV2?qdata=Q0I1ODYzQUNEMzJEQTUwMEQ5REVEMEYxRTkxODI0QjUuY0dGeVlXMGZSRE0wUWtZME9USXRNalE1UXkwME5EUXdMVGd5TXprdE5EUTJPRE5FTmtNeU1UUXpIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS6a6i7FinM36z3jXFHvbECtTaFTPfDc%2BX94aucuKr%2BsV0osoifxr9oSVUgFNEUqOBwzGpHEZGAnnyTRydH7yu4Wj%2B67Ljn6iJADL%2Bz9Yc%2BiYQt2z%2BiT4QDem5tf2ilnpfAal6lJ1f1EMCN7LM1B%2BZqK1azsjOFvo9suEWgxZtgfJiTe4Rkp31w/CrWigchx2PYsrgLZvGuNzcBJpD4uakEvEF8bmSwTw%2BTgveWW9gEgNfvkJzTP4P6dI%2BPY7MzLGm0I5PiRcFJiPc0sbB1UVhZvi2vxSC3zQ5ePpwlUzWUCMRcIopwERiA0xOoMVXzteE%2BUpsGx%2B%2Bc88LoVNf5CsRzm/kyREXZc90nsF6/5IzQjRgyYNP4COu%2Bj/7LNzg99fu9wy0QtRAOUnTlSJgj3C0Nzs1mAAfZ0S8WYShh3xN6lmZXUrCZIsbQIUElgmtmBbqGnoyBUf9BJ0gXbjX5WsJvy6yMuBVQsNryW3bKxM/L875DtGakV3wsDVfQ6m6B6DbWeC0q7TzK/uJD2OKJtuOwRDfYINoEUA%2BMQsLZCKgu1gW4UPIJTpQ71t3zYPpMt5LVHu%2BGyJg0X3Av/zetf4R4ZDzb0PCCvk0cj68JlA4tmHnC9EQTDJfMCWIloW%2BMe6SAEQKa80Z7z0yoWkDM72iUpZ9tueuRPAm1cXzeHQ/8y9wyhpsN0Et73DhOZVhZCeg5sLVCOiV6f852Ny9n3XsL/uv2KUWSob7i%2Baolwn%2BDvc5%2BLtmb%2Bkdyt4bWv06kzefeMET0xWiVA2W%2Bh5a7r0L3tbFHtYNVBkmlQWnsvHcGBNHI%3D'


# type gaoxiao keji tiyu yule lishi junshi sannong meishi qiwen qiche xinlixue youxi redian
map = {'redian':redian,'keji':keji,'tiyu':tiyu,'lishi':lishi,'junshi':junshi,'sannong':sannong,'qiche':qiche,'xinlixue':xinliceshi,'youxi':youxi}

path = makedirs('news', 'qtt')
db = getdb()
for index in range(1, 100000):
    for k, v in map.items():
        content = requests.get(v).content.decode('utf-8')
        datas = json.loads(content)['data']['data']
        for data in datas:
            try:
                # 文章url
                share_url = data['share_url']
                title = data['title']
                read_count = int(data['read_count'])
                if read_count < 500:
                    continue
                if not data['tips'] == '':
                    continue
                print(F'{read_count}    {title}')
                # read_count = int(read_count/10000)
                # 简介
                introduction = data['introduction']
                cover = data['cover']
                cover_all = ''
                if len(cover)>0:
                    for cc in cover:
                        cover_all += cc
                        cover_all += ';'
                news_content = requests.get(share_url).content.decode('utf-8')
                divs = etree.HTML(news_content).xpath('/html/body/section[1]/div/div[2]/p')
                txt = []
                for div in divs:
                    text = div.xpath('./text()')
                    src = div.xpath('./img/@data-src')
                    if len(text) > 0:
                        txt.append(text[0])
                        txt.append('\n')
                    if len(src) > 0:
                        txt.append(src[0])
                        txt.append('\n')
                save_db(db,title=title,intro=introduction,type=k,cover=cover_all,content=''.join(txt),url=share_url,play=read_count,author=data['nickname'],author_img=data['avatar'],data = time.strftime("%Y/%m/%d %H:%M", time.localtime(data['show_time'])))
                # news_path = F'{path}/{title}.txt'
                # savenews(news_path,''.join(txt))
                # upload_news(news_path)
            except Exception as e:
                print(e)
        time.sleep(4)
    print(F'趣头条 新闻爬虫 {index}    次完成！')
closedb(db)
