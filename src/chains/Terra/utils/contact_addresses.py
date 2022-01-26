#!/usr/bin/python3

# https://assets.terra.money/cw20/tokens.json
# https://assets.terra.money/cw20/contracts.json

class contract_addresses:
    def contact_addresses(network):
        if network == 'MAINNET':
            # columbus-5
            contracts = {
                # TerraSwap
                'TerraSwap_Factory': 'terra1ulgw0td86nvs4wtpsc80thv6xelk76ut7a7apj',
                'TerraSwap_Router': 'terra19qx5xe6q9ll4w0890ux7lv2p4mf3csd4qvt3ex',
                # Mirror https://docs.mirror.finance/networks#terra
                'Collector': 'terra1s4fllut0e6vw0k3fxsg4fs6fm2ad6hn0prqp3s',
                'Community': 'terra1x35fvy3sy47drd3qs288sm47fjzjnksuwpyl9k',
                'Factory': 'terra1mzj9nsxx0lxlaxnekleqdy8xnyw2qrh3uz6h8p',
                'Mirror Governance': 'terra1wh39swv7nq36pnefnupttm2nr96kz7jjddyt2x',
                'Mint': 'terra1wfz7h3aqf4cjmjcvc6s8lxdhh7k30nkczyf0mj',
                'Oracle': 'terra1t6xe0txzywdg85n6k8c960cuwgh6l8esw6lau9',
                'MirrorStaking': 'terra17f7zu97865jmknk7p2glqvxzhduk78772ezac5',
                'Airdrop': 'terra1kalp2knjm4cs3f59ukr4hdhuuncp648eqrgshw',
                'Limit Order': 'terra1zpr8tq3ts96mthcdkukmqq4y9lhw0ycevsnw89',
                'Collateral Oracle': 'terra1pmlh0j5gpzh2wsmyd3cuk39cgh2gfwk6h5wy9j',
                'Lock': 'terra169urmlm8wcltyjsrn7gedheh7dker69ujmerv2',
                'Short Reward': 'terra16mlzdwqq5qs6a23250lq0fftke8v80sapc5kye',
                'Mirror MIR-UST Pair': 'terra1amv303y8kzxuegvurh0gug2xe9wkgj65enq2ux',
                'Mirror MIR-UST LP': 'terra17gjf2zehfvnyjtdgua9p9ygquk6gukxe7ucgwh',
                # mAssets https://docs.mirror.finance/networks#terra
                'aUST' : 'terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu',
                'bETH' : 'terra1dzhzukyezv0etz22ud940z7adyv7xgcjkahuun',
                'bLUNA' : 'terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp',
                'LOTA' : 'terra1ez46kxtulsdv07538fh5ra5xj8l68mu8eg24vr',
                'mAAPL' : 'terra1vxtwu4ehgzz77mnfwrntyrmgl64qjs75mpwqaz',
                'mABNB' : 'terra1g4x2pzmkc9z3mseewxf758rllg08z3797xly0n',
                'mAMC' : 'terra1qelfthdanju7wavc5tq0k5r0rhsyzyyrsn09qy',
                'mAMD' : 'terra18ej5nsuu867fkx4tuy2aglpvqjrkcrjjslap3z',
                'mAMZN' : 'terra165nd2qmrtszehcfrntlplzern7zl4ahtlhd5t2',
                'mARKK' : 'terra1qqfx5jph0rsmkur2zgzyqnfucra45rtjae5vh6',
                'mBABA' : 'terra1w7zgkcyt7y4zpct9dw8mw362ywvdlydnum2awa',
                'mBTC' : 'terra1rhhvx8nzfrx5fufkuft06q5marfkucdqwq5sjw',
                'mCOIN' : 'terra18wayjpyq28gd970qzgjfmsjj7dmgdk039duhph',
                'mDOT' : 'terra19ya4jpvjvvtggepvmmj6ftmwly3p7way0tt08r',
                'mETH' : 'terra1dk3g53js3034x4v5c3vavhj2738une880yu6kx',
                'mFB' : 'terra1mqsjugsugfprn3cvgxsrr8akkvdxv2pzc74us7',
                'mGLXY' : 'terra1l5lrxtwd98ylfy09fn866au6dp76gu8ywnudls',
                'mGME' : 'terra1m6j6j9gw728n82k78s0j9kq8l5p6ne0xcc820p',
                'mGOOGL' : 'terra1h8arz2k547uvmpxctuwush3jzc8fun4s96qgwt',
                'mGS' : 'terra137drsu8gce5thf6jr5mxlfghw36rpljt3zj73v',
                'mHOOD' : 'terra18yqdfzfhnguerz9du5mnvxsh5kxlknqhcxzjfr',
                'mIAU' : 'terra10h7ry7apm55h4ez502dqdv9gr53juu85nkd4aq',
                'MINE' : 'terra1kcthelkax4j9x8d3ny6sdag0qmxxynl3qtcrpy',
                'MIR' : 'terra15gwkyepfc6xgca5t5zefzwy42uts8l2m4g40k6',
                'mMSFT' : 'terra1227ppwxxj3jxz8cfgq00jgnxqcny7ryenvkwj6',
                'mNFLX' : 'terra1jsxngqasf2zynj5kyh0tgq9mj3zksa5gk35j4k',
                'mQQQ' : 'terra1csk6tc7pdmpr782w527hwhez6gfv632tyf72cp',
                'mSLV' : 'terra1kscs6uhrqwy6rx5kuw5lwpuqvm3t6j2d6uf2lp',
                'mSPY' : 'terra1aa00lpfexyycedfg5k2p60l9djcmw0ue5l8fhc',
                'mSQ' : 'terra1u43zu5amjlsgty5j64445fr9yglhm53m576ugh',
                'mTSLA' : 'terra14y5affaarufk3uscy2vr6pe6w6zqf2wpjzn5sh',
                'mTWTR' : 'terra1cc3enj9qgchlrj34cnzhwuclc4vl2z3jl7tkqg',
                'mUSO' : 'terra1lvmx8fsagy70tv0fhmfzdw9h6s3sy4prz38ugf',
                'mVIXY' : 'terra19cmt6vzvhnnnfsmccaaxzy2uaj06zjktu6yzjx',
                'SPEC' : 'terra1s5eczhe0h0jutf46re52x5z4r03c8hupacxmdr',
                'STT' : 'terra13xujxcrc9dqft4p9a8ls0w3j0xnzm6y2uvve8n',
                'TWD' : 'terra19djkaepjjswucys4npd5ltaxgsntl7jf0xz7w6',
                # Spectrum Protocol
                # https://github.com/spectrumprotocol/frontend/blob/11de02569898be54abc716b5a651cbf064865db5/src/app/consts/networks.ts
                'mirrorFarm': 'terra1kehar0l76kzuvrrcwj5um72u3pjq2uvp62aruf',
                'anchorFarm': 'terra1fqzczuddqsdml37a20pysjx5wk9dh4tdzu2mrw',
                'specFarm': 'terra17hjvrkcwn3jk2qf69s5ldxx5rjccchu35assga',
                'pylonFarm': 'terra1r3675psl7s2fe0sfh0vut5z4hrywgyyfdrzg95',
                'specgov': 'terra1dpe4fmcz2jqk6t50plw0gqa2q3he2tj6wex5cl',
                'SpectrumStaking' : 'terra1fxwelge6mf5l6z0rjpylzcfq9w9tw2q7tewaf5',
                'Spectrum SPEC-UST Pair': 'terra1tn8ejzw8kpuc87nu42f6qeyen4c7qy35tl8t20',
                'Spectrum SPEC-UST LP' : 'terra1y9kxxm97vu4ex3uy0rgdr5h2vt7aze5sqx7jyl',
                # Anchor
                # https://docs.anchorprotocol.com/smart-contracts/deployed-contracts
                'ANC': 'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76',
                'bLunaHub': 'terra1mtwph2juhj0rvjz7dy92gvl6xvukaxu8rfv8ts',
                'bLunaReward': 'terra17yap3mhph35pcwvhza38c2lkj7gzywzy05h7l0',
                'bLunaAirdrop': 'terra199t7hg7w5vymehhg834r6799pju2q3a0ya7ae9',
                'mmInterestModel': 'terra1kq8zzq5hufas9t0kjsjc62t2kucfnx8txf547n',
                'mmOracle': 'terra1cgg6yef7qcdm070qftghfulaxmllgmvk77nc7t',
                'mmMarket': 'terra1sepfj7s0aeg5967uxnfk4thzlerrsktkpelm5s',
                'mmOverseer': 'terra1tmnqgvg567ypvsvk6rwsga3srp7e3lg6u0elp8',
                'mmCustody': 'terra1ptjp2vfjrwh0j0faj9r6katm640kgjxnwwq9kn',
                'mmLiquidation': 'terra1w9ky73v4g7v98zzdqpqgf3kjmusnx4d4mvnac6',
                'mmDistributionModel': 'terra14mufqpr5mevdfn92p4jchpkxp7xr46uyknqjwq',
                'aTerra': 'terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu',
                'terraswapblunaLunaPair': 'terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p',
                'terraswapblunaLunaLPToken': 'terra1nuy34nwnsh53ygpc4xprlj263cztw7vc99leh2',
                'terraswapAncUstPair': 'terra1gm5p3ner9x9xpwugn9sp6gvhd0lwrtkyrecdn3',
                'terraswapAncUstLPToken': 'terra1gecs98vcuktyfkrve9czrpgtg0m3aq586x6gzm',
                'Anchor Governance': 'terra1f32xyep306hhcxxxf7mlyh0ucggc00rm2s9da5',
                'distributor': 'terra1mxf7d5updqxfgvchd7lv6575ehhm8qfdttuqzz',
                'collector': 'terra14ku9pgw5ld90dexlyju02u4rn6frheexr5f96h',
                'community': 'terra12wk8dey0kffwp27l5ucfumczlsc9aned8rqueg',
                'Anchor Staking': 'terra1897an2xux840p9lrh6py3ryankc6mspw49xse3',
                'airdrop': 'terra146ahqn6d3qgdvmj8cj96hh03dzmeedhsf0kxqm',
                'team_vesting': 'terra1pm54pmw3ej0vfwn3gtn6cdmaqxt0x37e9jt0za',
                'investor_vesting': 'terra10evq9zxk2m86n3n3xnpw28jpqwp628c6dzuq42',
                'success_tx_hash': '42DE8348A333613EB013251DE2056EE301019DA8C2505935B24E8596AFD350A1',
                'failed_tx_hash': '004DE6AFAD74853F89B2BFA1DF0B286692FA1D504AD7B9327E03D670C47E93D3',
                # Nexus
                # https://docs.nexusprotocol.app/launch/smart-contracts/deployed-contracts
                'PSI' : 'terra12897djskt9rge8dtmm86w654g7kzckkd698608',
                'nLUNA': 'terra10f2mt82kjnkxqj2gepgwl637u2w4ue2z5nhz5j',
                'NexusnETHrewards' : 'terra1fhqsu40s0lk3p308mcakzjecj6ts6j2guepfr4',
                'NexusnLUNArewards' : 'terra1hjv3quqsrw3jy7pulgutj0tgxrcrnw2zs2j0k7',
                'Nexus bLuna Vault' : 'terra1cda4adzngjzcn8quvfu2229s8tedl5t306352x',
                'Nexus Governance' : 'terra1xrk6v2tfjrhjz2dsfecj40ps7ayanjx970gy0j',
                'Nexus Psi-UST Pair' : 'terra163pkeeuwxzr0yhndf8xd2jprm9hrtk59xf7nqf',
                'Nexus Psi-UST LP' : 'terra1q6r8hfdl203htfvpsmyh8x689lp2g0m7856fwd',
                'Nexus Psi-UST Staking' : 'terra12kzewegufqprmzl20nhsuwjjq6xu8t8ppzt30a',
                'Nexus nLuna+Psi Pair' : 'terra1zvn8z6y8u2ndwvsjhtpsjsghk6pa6ugwzxp6vx',
                'Nexus nLuna+Psi LP' : 'terra1tuw46dwfvahpcwf3ulempzsn9a0vhazut87zec',
                'Nexus nLuna+Psi Staking' : 'terra1hs4ev0ghwn4wr888jwm56eztfpau6rjcd8mczc',
                'Nexus Psi for ANC stakers': 'terra1992lljnteewpz0g398geufylawcmmvgh8l8v96',
                # Glow
                # https://docs.glowyield.com/glow-yield/smart-contracts/deployed-contracts
                'GLOW': 'terra13zx49nk8wjavedjzu8xkk95r3t0ta43c9ptul7',
                'Glow Gov' : 'terra1xxp34xk4rjexwlu0xfdhyn0zr3qsgare04yll0',
                'Glow GLOW-UST Pair': 'terra1p44kn7l233p7gcj0v3mzury8k7cwf4zt6gsxs5',
                'Glow GLOW-UST LP': 'terra1khm4az2cjlzl76885x2n7re48l9ygckjuye0mt',
                'Glow Staking' : 'terra1le3a67j4khkjhyytkllxre60dvywm43ztq2s8t',
                # Astroport
                # https://docs.astroport.fi/astroport/smart-contracts/astroport-contract-addresses
                'ASTRO': 'terra1xj49zyqrwpv5k928jwfpfy2ha668nwdgkwlrg3',
                'Astroport ASTRO-UST Pool': 'terra1l7xu2rl3c7qmtx3r5sd2tz25glf6jh8ul7aag7',
                'Astroport ASTRO-UST LP': 'terra17n5sunn88hpy965mzvt3079fqx3rttnplg779g',
                'Astroport Psi-UST Pool': 'terra1v5ct2tuhfqd0tf8z0wwengh4fg77kaczgf6gtx',
                'Astroport Psi-UST LP': 'terra1cspx9menzglmn7xt3tcn8v8lg6gu9r50d7lnve',
                'Astroport bLUNA-LUNA Pool': 'terra1j66jatn3k50hjtg2xemnjm8s7y8dws9xqa5y8w',
                'Astroport bLUNA-LUNA LP': 'terra1htw7hm40ch0hacm8qpgd24sus4h0tq3hsseatl',
                'Astroport Staking' : '',
                'Astroport Lockdrop' : 'terra1627ldjvxatt54ydd3ns6xaxtd68a2vtyu7kakj', # Phase 1
                'Astroport Auction' : 'terra1tvld5k6pus2yh7pcu7xuwyjedn7mjxfkkkjjap', # Phase 2
                'Astroport Generator' : 'terra1zgrx9jjqrfye8swykfgmd6hpde60j0nszzupp9',
                # Valkyrie
                # https://docs.valkyrieprotocol.com/deployed-contracts
                'VKR': 'terra1dy9kmlm4anr92e42mrkjwzyvfqwz66un00rwr5',
                'Valkyrie Governance': 'terra1w6xf64nlmy3fevmmypx6w2fa34ue74hlye3chk',
                # ApolloDAO
                'APOLLO': 'terra100yeqvww74h4yaejj6h733thgcafdaukjtw397',
                'Apollo DAO Warchest': 'terra1hxrd8pnqytqpelape3aemprw3a023wryw7p0xn',
                'Apollo Factory': 'terra1g7jjjkt5uvkjeyhp8ecdz4e4hvtn83sud3tmh2',
                'Apollo MINE-UST AutoCompounder': 'terra15cy5ef4e5mtxtjrjemkhlf2jjal7zmzug45vy8',
                # LOOP
                'LOOP': 'terra1nef5jf6c7js9x6gkntlehgywvjlpytm7pcgkn4',
                'LOOPR': 'terra1jx4lmmke2srcvpjeereetc9hgegp4g5j0p9r2q',
                # Pylon
                'Pylon bPsiDP-24m Token': 'terra1zsaswh926ey8qa5x4vj93kzzlfnef0pstuca0y',
                # TerraSwap
                'Terraswap Pylon MINE-UST Pair': 'terra178jydtjvj4gw8earkgnqc80c3hrmqj4kw2welz',
                'Terraswap Pylon MINE-UST LP': 'terra1rqkyau9hanxtn63mjrdfhpnkpddztv3qav0tq2'
            }
        else:
            # bombay-12
            contracts = {
                # TerraSwap
                'TerraSwap_Factory': 'terra18qpjm4zkvqnpjpw0zn0tdr8gdzvt8au35v45xf',
                'TerraSwap_Router': 'terra14z80rwpd0alzj4xdtgqdmcqt9wd9xj5ffd60wp',
                # Mirror https://docs.mirror.finance/networks#terra
                'Collector': 'terra1v046ktavwzlyct5gh8ls767fh7hc4gxc95grxy',
                'Community': 'terra10qm80sfht0zhh3gaeej7sd4f92tswc44fn000q',
                'Factory': 'terra10l9xc9eyrpxd5tqjgy6uxrw7dd9cv897cw8wdr',
                'Gov': 'terra12r5ghc6ppewcdcs3hkewrz24ey6xl7mmpk478s',
                'Mint': 'terra1s9ehcjv0dqj2gsl72xrpp0ga5fql7fj7y3kq3w',
                'Oracle': 'terra1uvxhec74deupp47enh7z5pk55f3cvcz8nj4ww9',
                'MirrorStaking': 'terra1a06dgl27rhujjphsn4drl242ufws267qxypptx',
                'Airdrop': 'terra1p6nvyw7vz3fgpy4nyh3q3vc09e65sr97ejxn2p',
                'Limit Order': 'terra1vc4ch0z3n6c23f9uywzy5yqaj2gmpnam8qgge7',
                'Collateral Oracle': 'terra1q3ls6u2glsazdeu7dxggk8d04elnvmsg0ung6n',
                'Lock': 'terra1pcxghd4dyf950mcs0kmlp7lvnrjsnl6qlfldwj',
                'Mirror MIR-UST Pair': 'terra1cz6qp8lfwht83fh9xm9n94kj04qc35ulga5dl0',
                'Mirror MIR-UST LP': 'terra1zrryfhlrpg49quz37u90ck6f396l4xdjs5s08j',
                # mAssets https://docs.mirror.finance/networks#terra
                'SPEC': 'terra1kvsxd94ue6f4rtchv2l6me5k07uh26s7637cza',
                'MIR': 'terra10llyp6v3j3her8u3ce66ragytu45kcmd9asj3u',
                'ANC': 'terra1747mad58h0w4y589y3sk84r5efqdev9q4r02pc',
                'aUST' : 'terra1ajt556dpzvjwl0kl5tzku3fc3p3knkg9mkv8jl',
                'bETH': 'terra19mkj9nec6e3y5754tlnuz4vem7lzh4n0lc2s3l',
                'bLUNA': 'terra1u0t35drzyy0mujj8rkdyzhe264uls4ug3wdp3x',
                'mAAPL': 'terra16vfxm98rxlc8erj4g0sj5932dvylgmdufnugk0',
                'mDOT': 'terra1fs6c6y65c65kkjanjwvmnrfvnm2s58ph88t9ky',
                'mGOOGL': 'terra1qg9ugndl25567u03jrr79xur2yk9d632fke3h2',
                'mGME': 'terra104tgj4gc3pp5s240a0mzqkhd3jzkn8v0u07hlf',
                'mGS': 'terra13myzfjdmvqkama2tt3v5f7quh75rv78w8kq6u6',
                'mTSLA': 'terra1nslem9lgwx53rvgqwd8hgq7pepsry6yr3wsen4',
                'mNFLX': 'terra1djnlav60utj06kk9dl7defsv8xql5qpryzvm3h',
                'mQQQ': 'terra18yx7ff8knc98p07pdkhm3u36wufaeacv47fuha',
                'mTWTR': 'terra1ax7mhqahj6vcqnnl675nqq2g9wghzuecy923vy',
                'mMSFT': 'terra12s2h8vlztjwu440khpc0063p34vm7nhu25w4p9',
                'mAMZN': 'terra12saaecsqwxj04fn0jsv4jmdyp6gylptf5tksge',
                'mBABA': 'terra15dr4ah3kha68kam7a907pje9w6z2lpjpnrkd06',
                'mIAU': 'terra19dl29dpykvzej8rg86mjqg8h63s9cqvkknpclr',
                'mSLV': 'terra1fdkfhgk433tar72t4edh6p6y9rmjulzc83ljuw',
                'mUSO': 'terra1fucmfp8x4mpzsydjaxyv26hrkdg4vpdzdvf647',
                'mVIXY': 'terra1z0k7nx0vl85hwpv3e3hu2cyfkwq07fl7nqchvd',
                'mFB': 'terra14gq9wj0tt6vu0m4ec2tkkv4ln3qrtl58lgdl2c',
                'mCOIN': 'terra1qre9crlfnulcg0m68qqywqqstplgvrzywsg3am',
                # Spectrum Protocol
                # https://github.com/spectrumprotocol/frontend/blob/11de02569898be54abc716b5a651cbf064865db5/src/app/consts/networks.ts
                'mirrorFarm': 'terra1hasdl7l6xtegnch8mjyw2g7mfh9nt3gtdtmpfu',
                'anchorFarm': 'terra1yvpd3j7mry7qrmmn2x9vapmr9qpzkvjgs4f7z7',
                'specFarm': 'terra1cedx8gpvu7c4vzfadwmf3pewg2030fqgw4q3dl',
                'pylonFarm': 'terra1hgjp2yjqe7ngzsx283tm7ch8xcsvk5c8mdj2tw',
                'specgov': 'terra1x3l2tkkwzzr0qsnrpy3lf2cm005zxv7pun26x4',
                'SpectrumStaking' : 'terra15nwqmmmza9y643apneg0ddwt0ekk38qdevnnjt',
                'Spectrum SPEC-UST Pair': 'terra15cjce08zcmempedxwtce2y44y2ayup8gww3txr',
                'Spectrum SPEC-UST LP' : 'terra1ntt4mdhr9lukayenntgltqppw4yy6hts7wr67d',
                # Anchor
                "bLunaHub": "terra1fflas6wv4snv8lsda9knvq2w0cyt493r8puh2e",
                "bLunaToken": "terra1u0t35drzyy0mujj8rkdyzhe264uls4ug3wdp3x",
                "bLunaReward": "terra1ac24j6pdxh53czqyrkr6ygphdeftg7u3958tl2",
                "bLunaAirdrop": "terra1334h20c9ewxguw9p9vdxzmr8994qj4qu77ux6q",
                "mmInterestModel": "terra1m25aqupscdw2kw4tnq5ql6hexgr34mr76azh5x",
                "mmOracle": "terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8",
                "mmMarket": "terra15dwd5mj8v59wpj0wvt233mf5efdff808c5tkal",
                "mmOverseer": "terra1qljxd0y3j3gk97025qvl3lgq8ygup4gsksvaxv",
                "mmCustody": "terra1ltnkx0mv7lf2rca9f8w740ashu93ujughy4s7p",
                "mmLiquidation": "terra16vc4v9hhntswzkuunqhncs9yy30mqql3gxlqfe",
                "mmDistributionModel": "terra1u64cezah94sq3ye8y0ung28x3pxc37tv8fth7h",
                "aTerra": "terra1ajt556dpzvjwl0kl5tzku3fc3p3knkg9mkv8jl",
                "terraswapblunaLunaPair": "terra13e4jmcjnwrauvl2fnjdwex0exuzd8zrh5xk29v",
                "terraswapblunaLunaLPToken": "terra1tj4pavqjqjfm0wh73sh7yy9m4uq3m2cpmgva6n",
                "terraswapAncUstPair": "terra1wfvczps2865j0awnurk9m04u7wdmd6qv3fdnvz",
                "terraswapAncUstLPToken": "terra1vg0qyq92ky9z9dp0j9fv5rmr2s80sg605dah6f",
                "gov": "terra16ckeuu7c6ggu52a8se005mg5c0kd2kmuun63cu",
                "distributor": "terra1z7nxemcnm8kp7fs33cs7ge4wfuld307v80gypj",
                "collector": "terra1hlctcrrhcl2azxzcsns467le876cfuzam6jty4",
                "community": "terra17g577z0pqt6tejhceh06y3lyeudfs3v90mzduy",
                "Anchor Staking": "terra19nxz35c8f7t3ghdxrxherym20tux8eccar0c3k",
                "ANC": "terra1747mad58h0w4y589y3sk84r5efqdev9q4r02pc",
                "airdrop": "terra1u5ywhlve3wugzqslqvm8ks2j0nsvrqjx0mgxpk",
                "investor_vesting": "not available in testnet",
                "team_vesting": "not available in testnet",
                'success_tx_hash': 'BC00BDD340F8622679A8746CC0AC3474D87D3189F4F7263A77C873D3A3D9ED17',
                'failed_tx_hash': 'E69D9B5B2325EE20B2194EB2A46A6584CC187F2FE2E0B2985774D1FD5810AE1E'
            }
        return contracts

    # Create a reverse dictionary to look up names for contracts
    def rev_contact_addresses(contact_addresses):
        rev_contact_addresses = dict((v, k) for k, v in contact_addresses.items())
        return rev_contact_addresses
